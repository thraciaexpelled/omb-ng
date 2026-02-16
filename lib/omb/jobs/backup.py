import os
import platform
import shutil
import sys
import time

from lib.status import status, status_tags, status_prompt_type
from lib.omb.textdata import textdata

class omb_backup:
  def __init__(self, args = None, source_is_caller = False):
    self.args = args
    self.source_is_caller = source_is_caller
    self.status = status()
    self.textdata = textdata()
    self.backup_directory = os.path.join(omb_backup.get_user_home_directory(), '.omb_backups')
  
  def do(self) -> int:
    if self.source_is_caller:
      self.status.push(status_tags.ok, 'starting backup job called by source')
      return self.do_bu_job()

    if self.args.clean:
      return self.clean()

    if self.args.restore:
      return self.restore()

    return self.do_bu_job()

  def do_bu_job(self) -> int:
    if not omb_backup.check_for_backup_folder():
      self.status.push(
        status_tags.give, 
        'creating backup directory in %s' % os.path.join(omb_backup.get_user_home_directory(), '.omb_backups')
      )

      try:
        os.mkdir(os.path.join(omb_backup.get_user_home_directory(), '.omb_backups'))
      except Exception as e:
        self.status.push(status_tags.fail, 'caught exception: %s' % e)
        return -1

    self.status.push(status_tags.ok, 'querying files eligible for backup')
    eligible_backup_files: list[str] = self.get_bash_files()
    self.status.push(status_tags.ok, 'got %d files' % len(eligible_backup_files))

    self.status.push(status_tags.ok, 'starting backup')
    bu: int = self.start_backup()
    self.status.push(status_tags.ok, 'backup job finished with code %d' % bu)

    return bu

  def clean(self) -> int:
    self.status.push(status_tags.ok, 'preparing for clean up duty')
    affirmation: str = self.status.push(status_tags.ok, 'clean %s?' % self.backup_directory, True)
    if affirmation.casefold() == 'y':
      self.status.push(status_tags.ok, 'removing backups')

      if not os.listdir(self.backup_directory):
        sys.stderr.write('there is nothing to do\n')
        return -1

      for backup in os.listdir(self.backup_directory):
        self.status.push(status_tags.take, 'removing %s' % backup)
        try:
          full_backup_directory: str = os.path.join(self.backup_directory, backup)
          shutil.rmtree(full_backup_directory)
        except Exception as e:
          self.status.push(status_tags.fail, 'cleaning failed: %s' % e)
          return -1
    else:
      self.status.push(status_tags.ok, 'aborted')
      os.abort()

  def restore(self) -> int:
    # self.status.push(status_tags.fail, 'this job is not implemented yet (restore)')
    backup_to_restore: str = self.choose_backups()
    affirmation: str = self.status.push(status_tags.ok, 'restore from backup %s?' % backup_to_restore, True)
    if affirmation.casefold() == 'y':
      self.status.push(status_tags.ok, 'restoring from %s' % backup_to_restore)
      backed_up_files: list[str] = os.listdir(os.path.join(self.backup_directory, backup_to_restore))
      for backed_up_file in backed_up_files:
        try:
          full_backed_up_file_directory: str = os.path.join(self.backup_directory, backup_to_restore, backed_up_file)
          self.status.push(status_tags.give, 'restoring %s' % backed_up_file)
          shutil.copy(full_backed_up_file_directory, omb_backup.get_user_home_directory())
        except Exception as e:
          self.status.push(status_tags.fail, 'restore failed: %s' % e)
          return -1
    else:
      self.status.push(status_tags.ok, 'aborted')
      os.abort()

    return 0

  def start_backup(self) -> int:
    timestamp: str = omb_backup.form_backup_timestamp()
    destination: str = os.path.join(omb_backup.get_user_home_directory(), '.omb_backups', f'bu;{timestamp}')

    try:
      timestamp = omb_backup.form_backup_timestamp()
      os.mkdir(destination)
    except Exception as e:
      self.status.push(status_tags.fail, 'backup failed: %s' % e)
      return -1

    for bash_file in self.get_bash_files():
      try:
        source = os.path.join(omb_backup.get_user_home_directory(), bash_file)
        self.status.push(status_tags.give, 'backing up %s' % bash_file)
        shutil.copy(source, destination)
      except Exception as e:
        self.status.push(status_tags.fail, 'backup failed: %s' % e)
        return -1
    
    return 0

  def get_bash_files(self) -> list[str]:
    files = [f for f in os.listdir(omb_backup.get_user_home_directory()) if not os.path.isdir(f)]
    dotfiles = [f for f in files if f.startswith('.')]
    return [f for f in dotfiles if 'bash' in f]

  def choose_backups(self) -> str:
    self.status.push(status_tags.ok, 'choose a backup')
    idx: int = self.list_backups()

    print()

    choice: int = int(self.status.push(status_tags.ok, 'selection:', True, status_prompt_type.anytype))
    try:
      full_backup_directory = os.path.join(self.backup_directory, os.listdir(self.backup_directory)[choice - 1])
      assert os.path.exists(full_backup_directory), 'whoopsies (%s does not exist) (this is a bug; report it to the issue tracker)' % full_backup_directory
      return full_backup_directory
    except IndexError:
      self.status.push(status_tags.fail, 'invalid choice')
      print()
      self.choose_backups()

  def list_backups(self) -> int:
    backups: list[str] = os.listdir(self.backup_directory)
    backups_and_epochs: dict = {}

    for (i, backup) in enumerate(backups):
      full_backup_directory = os.path.join(self.backup_directory, backup)
      backups_and_epochs[backup] = omb_backup.epoch(full_backup_directory)

    epochs = backups_and_epochs.values()
    try:
      min_epoch = min(epochs)
      max_epoch = max(epochs)
    except ValueError:
      print('\tempty\n\trun `omb backup` to start backing up')
      return ""

    print()

    counter = 0
    for (backup, backup_epoch) in backups_and_epochs.items():
      counter += 1
      if backup_epoch == min_epoch:
        print('  %d  %s (oldest)' % (counter, backup.replace('bu;', '')))
      elif backup_epoch == max_epoch:
        print('  %d  %s (newest)' % (counter, backup.replace('bu;', '')))
      else:
        print('  %d  %s' % (counter, backup.replace('bu;', '')))

    # counter should effectively be equal to the length of backup
    return counter if counter == len(backups) else len(backups)
  
  @staticmethod
  def epoch(file) -> int:
    timestamp = 0
    if platform.system() == 'Windows':
      timestamp = os.path.getctime(path_to_file)
    else:
      stat = os.stat(file)
      try:
        timestamp = stat.st_birthtime
      except AttributeError:
        timestamp = stat.st_mtime
    return timestamp

  @staticmethod
  def form_backup_timestamp() -> str:
    return time.strftime('%H%M%S-%Y%m%d')

  @staticmethod
  def check_for_backup_folder() -> bool:
    return os.path.exists(os.path.join(omb_backup.get_user_home_directory(), '.omb_backups'))

  @staticmethod
  def get_user_home_directory() -> str:
    return os.getenv('HOME')
    
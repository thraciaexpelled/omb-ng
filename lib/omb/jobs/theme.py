import os
import sys

from lib.status import status, status_tags, status_prompt_type
from lib.omb.textdata import textdata
from lib.omb.jobs.backup import omb_backup

class omb_themer:
  def __init__(self, arg):
    self.arg = arg
    self.status = status()
    self.theme_directory = os.path.join(omb_themer.get_user_home_directory(), '.omb_themes')
    self.bashrc_location = os.path.join(omb_themer.get_user_home_directory(), '.bashrc')
    self.bu = omb_backup(None, True)

  def do(self) -> int:
    # TODO: find a way to do this without using if-statements
    if self.arg.set:
      return self.set()
    elif self.arg.unset:
      return self.unset()
    elif self.arg.info:
      return self.info()
    elif self.arg.list()
      return self.list()
    else:
      sys.stderr.write('there is nothing to do\n')
      return -1

  # omb theme -s
  def set(self) -> int:
    target_theme: str = self.arg.set
    stylish_theme: str = omb_themer.classy(target_theme)
    themes: list[str] = []
    first_time_invocation: bool = False

    self.status.push(status_tags.ok, 'finding theme %s' % stylish_theme)

    try:
      for theme_file in os.listdir(self.theme_directory):
        themes.append(theme_file.removesuffix('.omb_theme.bash'))
    except Exception:
      self.status.push(status_tags.ok, 'initializing')
      try:
        os.mkdir(self.theme_directory)
        return self.set()
      except Exception as e:
        self.status.push(status_tags.fail, 'initialization failed: %s' % e)
        return -1

    if target_theme not in themes:
      self.status.push(status_tags.fail, 'theme %s not found' % f'\x1b[1m\x1b[4m{target_theme}\x1b[0m')
      self.status.push(status_tags.fail, 'online installation is not implemented yet')
      return 1
    
    invocation_line: int = self.get_omb_theme_invocation_line()
    if invocation_line == -1:
      first_time_invocation = True

    if first_time_invocation:
      self.status.push(status_tags.ok, 'preparing for first theme setting')
      self.status.push(status_tags.ok, 'starting a backup (bu :3)')
      assert self.bu.do() == 0, "bu job failed rofl"
      self.status.push(status_tags.give, 'setting theme %s' % stylish_theme)

      try:
        with open(self.bashrc_location, 'a') as bashrc:
          bashrc.write('\n')
          bashrc.write('# omb theme\n')
          bashrc.write('source %s\n' % os.path.join(self.theme_directory, f'{target_theme}.omb_theme.bash'))
          bashrc.write('# omb theme end')
      except Exception as e:
        self.status.push(status_tags.fail, 'failed to set theme %s: %s' % (stylish_theme, e))
        return -1
    else:
      self.status.push(status_tags.ok, 'starting a backup (bu :3)')
      assert self.bu.do() == 0, "bu job failed rofl"
      # apparently this should just work lol
      self.status.push(status_tags.give, 'setting theme %s' % stylish_theme)
      try:
        with open(self.bashrc_location, 'r') as bashrc:
          lines: list = bashrc.readlines()
      
        if lines[invocation_line + 1] == 'source %s\n' % os.path.join(self.theme_directory, f'{target_theme}.omb_theme.bash'):
          self.status.push(status_tags.fail, 'theme %s is already set' % stylish_theme)
          return -1

        lines[invocation_line + 1] = 'source %s\n' % os.path.join(self.theme_directory, f'{target_theme}.omb_theme.bash')

        with open(self.bashrc_location, 'w') as bashrc:
          bashrc.writelines(lines)
      except Exception as e:
        self.status.push(status_tags.fail, 'failed to set theme %s: %s' % (stylish_theme, e))
        return -1

    self.status.push(status_tags.ok, 'run %s to commit changes' % f'\x1b[1m\x1b[4msource {omb_themer.get_user_home_directory()}/.bashrc\x1b[0m')
    return 0

  def get_omb_theme_invocation_line(self) -> int:
    with open(self.bashrc_location, 'r') as bashrc:
      for i, line in enumerate(bashrc):
        if line.strip() == "# omb theme":
          return i

    return -1

  # omb theme -u
  def unset(self) -> int:
    invocation_line: int = self.get_omb_theme_invocation_line()

    if invocation_line == -1:
      self.status.push(status_tags.fail, 'no theme is set')
      self.status.push(status_tags.ok, 'run %s to set a theme' % f'\x1b[1m\x1b[4m{sys.argv[0]} theme --set <theme>\x1b[0m')
      return -1

    self.status.push(status_tags.take, 'unsetting current theme')
    try:
      with open(self.bashrc_location, 'r') as bashrc:
        lines: list = bashrc.readlines()
      
      if not lines[invocation_line + 1]:
        self.status.push(status_tags.fail, 'no theme is set')
        self.status.push(status_tags.ok, 'run %s to set a theme' % f'\x1b[1m\x1b[4m{sys.argv[0]} theme --set <theme>\x1b[0m')
        return -1

      lines[invocation_line + 1] = ''

      with open(self.bashrc_location, 'w') as bashrc:
        bashrc.writelines(lines)
    except Exception as e:
      self.status.push(status_tags.fail, 'failed to unset current theme %s' % e)
      return -1
    return 0

  # omb theme -i
  def info(self) -> int:
    target_theme: str = self.arg.info
    theme_filepath: str = os.path.join(self.theme_directory, f'{target_theme}.omb_theme.bash')
    theme_info: dict = omb_themer.simple_keyval(omb_themer.mini_head(theme_filepath, 5))

    self.status.push(status_tags.ok, 'theme %s (name in file: %s)' % (omb_themer.classy(target_theme), omb_themer.classy(theme_info["OMB_THEME_NAME"])))
    self.status.push(status_tags.ok, 'author: %s' % omb_themer.classy(theme_info["OMB_THEME_AUTHOR"]))
    self.status.push(status_tags.ok, 'version: %s' % omb_themer.classy(theme_info["OMB_THEME_VERSION"]))
    self.status.push(status_tags.ok, 'description: %s' % theme_info["OMB_THEME_DESCRIPTION"])

    return -1

  @staticmethod
  def simple_keyval(source: str) -> dict:
    result: dict = {}
    for line in source.split('\n'):
      if not line.strip():
        continue
      if '=' not in line:
        if line[0] == '#' and line[1] == '!':
          continue
        else:
          status().push(status_tags.fail, 'invalid syntax in source (%s)' % line)
          sys.exit(-1)

      key: str = line.split('=')[0]
      value: str = line.split('=')[1].replace('"', '')
      result[key] = value

    return result

  @staticmethod
  def mini_head(filename: str, n: int) -> str:
    result: str = ""
    with open(filename, 'r') as file:
      for i, line in enumerate(file):
        if not line.strip():
          i += 1
        result += line
        result += '\n'
        if i == n:
          return result

    return result

  @staticmethod
  def classy(s: str) -> int:
    return f'\x1b[1m\x1b[4m{s}\x1b[0m'

  @staticmethod
  def get_user_home_directory() -> str:
    return os.getenv('HOME')
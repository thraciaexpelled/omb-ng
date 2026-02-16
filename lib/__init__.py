import sys
import argparse as ap

from lib.omb.jobs.theme import omb_themer
from lib.omb.jobs.backup import omb_backup
from lib.omb.textdata import textdata

class omb_runtime:
  def __init__(self, argv):
    self.argv = argv
    self.textdata = textdata
    self.version = "0.9.0"

    if sys.platform == 'win32':
      sys.stderr.write('%s\n' % textdata.sub_backup.prog_backup_win32)

  def start_runtime(self) -> int:
    print('%s %s\n' % (__import__('os').path.basename(sys.argv[0]), self.version))

    ps = ap.ArgumentParser(
      prog='oh-my-bash',
      description=self.textdata.prog_description,
      epilog=self.textdata.prog_epilog
    )

    sp = ps.add_subparsers(dest='subcommand')

    (theme, backup) = (
      sp.add_parser('theme', help=self.textdata.sub_theme.prog_help),
      sp.add_parser('backup', help=self.textdata.sub_backup.prog_help)
    )

    # omb theme --set <name>
    theme.add_argument(
      '--set', '-s', type=str, help=self.textdata.sub_theme.prog_help_theme_set
    )

    # omb theme --unset
    theme.add_argument(
      '--unset', '-u', action='store_true', help=self.textdata.sub_theme.prog_help_theme_unset
    )

    # omb theme --info
    theme.add_argument(
      '--info', '-i', type=str, help=self.textdata.sub_theme.prog_help_theme_info
    )

    # omb backup --clean
    backup.add_argument(
      '--clean', '-c', action='store_true', help=self.textdata.sub_backup.prog_help_backup_clean
    )

    # omb backup --restore
    backup.add_argument(
      '--restore', '-r', action='store_true', help=self.textdata.sub_backup.prog_help_backup_restore
    )

    args = ps.parse_args(self.argv)

    match args.subcommand:
      case 'theme':
        job = omb_themer(args)
        return job.do()
      case 'backup':
        job = omb_backup(args)
        return job.do()
        return 0

    # nothing's happening
    sys.stderr.write('there is nothing to do\n')
    return -1
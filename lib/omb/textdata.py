class textdata:
  prog_description = 'Bash theme and plugin manager'
  prog_epilog = 'Yet another CLANGALICIOUS!™ creation'

  class sub_theme:
    prog_help = 'Install/Uninstall, Set/Unset themes'
    prog_help_theme_set = 'Set specified theme, installs theme if not found globally'
    prog_help_theme_unset = 'Unspecify current theme, restoring system\'s default Bash prompt'
    prog_help_theme_info = 'Get information about a theme'
    prog_help_theme_list = 'List themes'

  class sub_backup:
    prog_help = 'Backup Bash dotfiles'
    prog_help_backup_clean = 'Remove all backups with the program seeking user affirmation'
    prog_help_backup_restore = 'Restore a backup of the user\'s choice'
    prog_backup_win32 = """
Message from oh-by-bash: We detected that you are running our software from the Microsoft Windows software platform. 
We recommend to install oh-my-bash in a GNUenv (MSYS2, Cygwin, MinGW) if problems persist.

CLANGALICIOUS!
    """
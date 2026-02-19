<h1 align='center'>A crash course on creating themes for <i>Oh My Bash, Next Generation!</i></h1>

## Introductory
omb-ng! theme files are Bash scripts that may improve, change or modify the UI/UX of Bash.

### This is the most simple omb-ng! theme possible
```bash
#!/usr/bin/env bash

OMB_THEME_NAME="my_theme"
OMB_THEME_AUTHOR="less"
OMB_THEME_DESCRIPTION="arch arch femboy minimal hyprland rust niri hyprland niri rice hyprland cachyos rice"
OMB_THEME_VERSION="26H2"

export PS1=" *  "
```

**Notice the first four variable declarations?** These are **required** (although not enforced as of >= `0.10.3`) as omb-ng! reads the first 4-5 lines of the theme file, and then parses the variables as metadata. omb-ng! will panic if any of those variables are invalid.

**

### Naming conventions
```
<theme name>.omb_theme.bash
```

Although it's not required to include `.omb_theme` in the file name, it should be good practice nonetheless to do so.
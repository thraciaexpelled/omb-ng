<h1 align='center'>Oh My Bash, Next Generation!</h1>
omb-ng! (Oh My Bash, Next Generation!) is a theme manager for GNU Bash.
It can backup, restore, set and unset themes.

# Installation and Usage

## Installing omb-ng!
Copy and paste this to a terminal window.
```commandline
git clone https://www.github.com/thraciaexpelled/omb-ng
cd omb-ng
./install.sh
```

## Using omb-ng!
### Backing up files
omb-ng! can back up any Bash related files in `~`.
omb-ng! also backs up files whenever a theme is about to be set.

```commandline
omb backup
```

### Restoring files
```commandline
omb backup --restore
```

**OR**, *(added in 0.11.0!)*
```commandline
omb restore
```

### Setting a theme
Theme ***clangalicious*** will be installed if said `y` to.

```commandline
omb theme --set clangalicious
```

`--set` can be shortened to `-s`.
```commandline
omb theme -s clangalicious
```

### Unsetting the current theme
```commandline
omb theme --unset
```

`--unset` can be shortened to `-u`.
```commandline
omb theme -u
```

# Creating themes
[HOW_TO_MAKE_THEMES.md](HOW_TO_MAKE_THEMES.md)

# License
MIT.

<h1 align='center'>CLANGALICIOUS!</h1>
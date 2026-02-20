<h1 align='center'>Oh My Bash, Next Generation!</h1>
omb-ng! (Oh My Bash, Next Generation!) is a theme manager for GNU Bash.

It can backup, restore, set and unset themes.

<h1 align='center'>Installation and Usage</h1>

## Installing omb-ng!
Copy and paste this to a terminal window.
```commandline
git clone https://www.github.com/thraciaexpelled/omb-ng
cd omb-ng
./install.sh
```

### Requirements
```
pygit2
```

Although omb-ng! tries to minimize the usage of dependencies as much as possible to ease the installation process, it still requires some dependencies (and especially `pip`, for installing these dependencies) in order for omb-ng! to work.

The install script will detect if the dependencies are installed, or if `pip` is installed in the system.

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
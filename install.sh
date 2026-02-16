#!/usr/bin/env bash

PREFIX="$HOME/.omb/bin"

echo "OMB: installing oh my bash..."
mkdir -p $PREFIX
mkdir -p $PREFIX/../lib
cp -rf lib/* $PREFIX/../lib
chmod 755 $PREFIX/../lib/*
cp -rf bin/* $PREFIX
chmod +x $PREFIX/*

function changes {
  echo "OMB: writing changes to .bashrc..."
  printf "\n# omb\n" >> $HOME/.bashrc
  printf "export PATH=\$PATH:%s\n" "$PREFIX" >> $HOME/.bashrc
  printf "# omb end\n" >> $HOME/.bashrc
}

function install_template_themes {
  echo "OMB: installing template themes"
  mkdir -p $HOME/.omb_themes
  cp -vrf extra/themes/* $HOME/.omb_themes
}

echo "OMB: install template themes? [yn] (case sensitive)"
read ANSWER

if [[ "$ANSWER" == 'y' ]]; then
  install_template_themes
fi

cat $HOME/.bashrc | grep "omb end" 1>/dev/null 2>/dev/null
if [[ $? -ne 0 ]]; then
  changes
  echo "OMB: restart your terminal/shell to commit changes"
fi
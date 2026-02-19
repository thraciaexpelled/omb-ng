#!/usr/bin/env bash

OMB_THEME_NAME="meaty-skeleton"
OMB_THEME_AUTHOR="thraciaexpelled"
OMB_THEME_VERSION="1.0"
OMB_THEME_DESCRIPTION="The author personally uses this"

export PS1='\[\e[33;1m\]\t\[\e[0m\] \[\e[32;1m\]\w\[\e[0m\] [\[\e[93;4m\]$?\[\e[0m\]]\n\\$ '

PROMPT_COMMAND="export PROMPT_COMMAND=echo"
alias clear="unset PROMPT_COMMAND; clear; PROMPT_COMMAND='export PROMPT_COMMAND=echo'"

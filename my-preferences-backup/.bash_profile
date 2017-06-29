#schem for guangwei
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export LC_ALL=en_US.UTF-8

#ps schem
#export PS1='\[\e[1;32m\][\u@\h \W]\$\[\e[0m\]'
#export PS1='\[\e[0;33m\]\u\[\e[0m\]@\[\e[0;32m\]\h\[\e[0m\]:\[\e[0;34m\]\w\[\e[0m\]\$ '
#export PS1='\[\e[0;32m\]\h\[\e[0m\]:\[\e[0;34m\]\w\[\e[0m\]\e[0;33m\]\u\[\e[0m\]\$ '

#colors schem
#export COLOR_NC='\e[0m' # No Color
#export COLOR_WHITE='\e[1;37m'
#export COLOR_BLACK='\e[0;30m'
#export COLOR_BLUE='\e[0;34m'
#export COLOR_LIGHT_BLUE='\e[1;34m'
#export COLOR_GREEN='\e[0;32m'
#export COLOR_LIGHT_GREEN='\e[1;32m'
#export COLOR_CYAN='\e[0;36m'
#export COLOR_LIGHT_CYAN='\e[1;36m'
#export COLOR_RED='\e[0;31m'
#export COLOR_LIGHT_RED='\e[1;31m'
#export COLOR_PURPLE='\e[0;35m'
#export COLOR_LIGHT_PURPLE='\e[1;35m'
#export COLOR_BROWN='\e[0;33m'
#export COLOR_YELLOW='\e[1;33m'
#export COLOR_GRAY='\e[0;30m'
#export COLOR_LIGHT_GRAY='\e[0;37m'

#export LS_COLORS="rs=0:di=01;34:ln=01;36:mh=00:pi=40;33"
#export LSCOLORS=exfxcxdxbxegedabagacad
#export LSCOLORS=GxFxCxDxBxegedabagaced
#export LSCOLORS=ExFxCxDxBxegedabagacad
#export TERM="xterm-color" 
export CLICOLOR=1

#git schem
source ~/.git-completion.bash

#command
alias ll="ls -l"

#grep schem
export GREP_OPTIONS="--color=auto"

#android
export ANDROID_HOME="$HOME/Library/Android/sdk"
export ANDROID_NDK_HOME="$HOME/Library/Android/android-ndk-r14"
export ANDROID_NDK=$ANDROID_NDK_HOME

export PATH=$ANDROID_NDK_HOME:$ANDROID_HOME/Platform-tools:$ANDROID_HOME/tools:$PATH

#















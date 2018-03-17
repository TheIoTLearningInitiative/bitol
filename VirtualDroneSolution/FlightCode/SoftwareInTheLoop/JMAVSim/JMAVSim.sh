#!/bin/sh

set -x

# =============================================================================
# Variables
# =============================================================================

export JMAVSIM_PID=$$
export JMAVSIM_PID_PATH="/tmp/jmavsim"
export JMAVSIM_ARGUMENT_ACTION=$1

export DIRECTORY_SOURCE=$HOME/src/
export DIRECTORY_PX4=$DIRECTORY_SOURCE/Firmware

# =============================================================================
# Functions
# =============================================================================

list_descendants ()
{
  local children=$(ps -o pid= --ppid "$1")
  for pid in $children
  do
    list_descendants "$pid"
  done
  echo "$children"
}

# =============================================================================
# Main
# =============================================================================

cd $HOME

if [ "$LOCAL_DEVICE" = "start" ]; then
    echo $JMAVSIM_PID > $JMAVSIM_PID_PATH
    cd $DIRECTORY_PX4
    make posix jmavsim
elif [ "$LOCAL_DEVICE" = "stop" ]; then
    cat $JMAVSIM_PID_PATH
    JMAVSIM_PID=kill $(list_descendants ${LOCAL_PID})
fi

cd $HOME

# End Of File

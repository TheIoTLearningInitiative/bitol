#!/bin/sh

set -x

# =============================================================================
# Variables
# =============================================================================

export QGROUNDCONTROL_PID=$$
export QGROUNDCONTROL_PID_PATH=$HOME/qgroundcontrol
export QGROUNDCONTROL_ARGUMENT_ACTION=$1
export QGROUNDCONTROL_FILE=$HOME/QGroundControl.AppImage

# =============================================================================
# Functions
# =============================================================================

shutdown() {
  # Get our process group id
  PGID=$(ps -o pgid=$1 | grep -o [0-9]*)
  echo $PGID

  # Kill it in a new new process group
  setsid kill -9 -$PGID
  exit 0
}

# =============================================================================
# Main
# =============================================================================

cd $HOME

if [ "$QGROUNDCONTROL_ARGUMENT_ACTION" = "start" ]; then
    echo $QGROUNDCONTROL_PID > $QGROUNDCONTROL_PID_PATH
    $QGROUNDCONTROL_FILE &
    sleep 
    JMAVSim.sh start &
elif [ "$QGROUNDCONTROL_ARGUMENT_ACTION" = "stop" ]; then
    JMAVSim.sh stop &
    QGROUNDCONTROL_PID=`cat $QGROUNDCONTROL_PID_PATH`
    #kill -- -$(ps -o pgid=$QGROUNDCONTROL_PID | grep -o [0-9]*)
    shutdown $QGROUNDCONTROL_PID
    trap "shutdown" SIGINT SIGTERM
fi

cd $HOME

# End Of File

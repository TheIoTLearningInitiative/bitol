#!/bin/sh

set -x

# =============================================================================
# Variables
# =============================================================================

export GROUNDCONTROLSTATION_PID=$$
export GROUNDCONTROLSTATION_PID_PATH=$HOME/groundcontrolstation
export GROUNDCONTROLSTATION_ARGUMENT_ACTION=$1

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

if [ "$GROUNDCONTROLSTATION_ARGUMENT_ACTION" = "start" ]; then
    echo $GROUNDCONTROLSTATION_PID > $GROUNDCONTROLSTATION_PID_PATH
    QGroundControl.sh start &
    sleep 1
    JMAVSim.sh start &
elif [ "$GROUNDCONTROLSTATION_ARGUMENT_ACTION" = "stop" ]; then
    JMAVSim.sh stop &
    QGroundControl.sh start &
    GROUNDCONTROLSTATION_PID=`cat $GROUNDCONTROLSTATION_PID_PATH`
    #kill -- -$(ps -o pgid=$GROUNDCONTROLSTATION_PID | grep -o [0-9]*)
    shutdown $GROUNDCONTROLSTATION_PID
    trap "shutdown" SIGINT SIGTERM
fi

cd $HOME

# End Of File

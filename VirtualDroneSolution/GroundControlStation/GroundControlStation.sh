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
    JMAVSim.sh start &
    sleep 1
    echo $GROUNDCONTROLSTATION_PID > $GROUNDCONTROLSTATION_PID_PATH
    QGroundControl.sh start
elif [ "$GROUNDCONTROLSTATION_ARGUMENT_ACTION" = "stop" ]; then
    QGroundControl.sh stop &
    GROUNDCONTROLSTATION_PID=`cat $GROUNDCONTROLSTATION_PID_PATH`
    #kill -- -$(ps -o pgid=$GROUNDCONTROLSTATION_PID | grep -o [0-9]*)
    shutdown $GROUNDCONTROLSTATION_PID
    trap "shutdown" SIGINT SIGTERM
    JMAVSim.sh stop &
fi

cd $HOME

# End Of File

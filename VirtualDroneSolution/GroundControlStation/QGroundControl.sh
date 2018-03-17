#!/bin/sh

set -x

# =============================================================================
# Variables
# =============================================================================

export QGROUNDCONTROL_PID=$$
export QGROUNDCONTROL_PID_PATH=$HOME/qgroundcontrol
export QGROUNDCONTROL_ARGUMENT_ACTION=$1
export QGROUNDCONTROL_FILE=$HOME/QGroundControl.AppImage"

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================

cd $HOME

if [ "$QGROUNDCONTROL_ARGUMENT_ACTION" = "start" ]; then
    echo $QGROUNDCONTROL_PID > $QGROUNDCONTROL_PID_PATH
    $QGROUNDCONTROL_FILE
elif [ "$QGROUNDCONTROL_ARGUMENT_ACTION" = "stop" ]; then
    QGROUNDCONTROL_PID=`cat $QGROUNDCONTROL_PID_PATH`
    kill -- -$(ps -o pgid=$QGROUNDCONTROL_PID | grep -o [0-9]*)
fi

cd $HOME

# End Of File

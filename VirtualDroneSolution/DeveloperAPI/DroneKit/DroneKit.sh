#!/bin/sh

set -x

# =============================================================================
# Variables
# =============================================================================

export DRONEKIT_PID=$$
export DRONEKIT_PID_PATH=$HOME/dronekit
export DRONEKIT_ARGUMENT_ACTION=$1
export DRONEKIT_DIRECTORY=$HOME/Bitol/VirtualDroneSolution/DeveloperAPI/DroneKit/
export DRONEKIT_PYTHON=$DRONEKIT_DIRECTORY/DroneKitPython.py
export DRONEKIT_PX4=$DRONEKIT_DIRECTORY/DroneKitPythonPx4.py

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================

cd $HOME

if [ "$DRONEKIT_ARGUMENT_ACTION" = "start" ]; then

    echo $DRONEKIT_PID > $DRONEKIT_PID_PATH
    
    # screen -dm -S dronekit-sitl dronekit-sitl copter --home=20.6207591,-103.3991668,30,0 &
    # JMAVSim.sh start &
    SimVehicle.sh start &
    sleep 10
    
    # screen -dm -S mavproxy mavproxy.py --master=tcp:127.0.0.1:5760 --out=udpout:127.0.0.1:14550 --out=udpout:127.0.0.1:14560
    # screen -dm -S mavproxy.py --master=udp:127.0.0.1:14550 --out=udpout:127.0.0.1:14570 --out=udpout:127.0.0.1:14580
    # None
    # sleep 10
    
    QGroundControl.sh start &
    sleep 10
    
    python $DRONEKIT_PYTHON
    
elif [ "$DRONEKIT_ARGUMENT_ACTION" = "stop" ]; then
    
    QGroundControl.sh stop &
    sleep 1
    JMAVSim.sh stop &
    sleep 1
    killall -9 dronekit-sitl
    sleep 1
    DRONEKIT_PID=`cat $DRONEKIT_PID_PATH`
    kill -- -$(ps -o pgid=$DRONEKIT_PID | grep -o [0-9]*)
    
fi

cd $HOME

# End Of File

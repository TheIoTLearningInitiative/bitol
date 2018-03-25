#!/bin/sh

set -x

# =============================================================================
# Variables
# =============================================================================

export GPS_PID=$$
export GPS_PID_PATH=$HOME/gps
export GPS_ARGUMENT_ACTION=$1
export GPS_DIRECTORY=$HOME/Bitol/VirtualDroneSolution/Features/GlobalPositioningSystem/

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================

cd $HOME

if [ "$GPS_ARGUMENT_ACTION" = "start" ]; then

    echo $GPS_PID > $GPS_PID_PATH
    
    # =========================================================================
    # SITL: DroneKit-Sitl <> PX4 Sitl JMAVSim <> Ardupilot Sitl SimVehicle
    # =========================================================================
    # screen -dm -S dronekit-sitl dronekit-sitl copter --home=$MAIN_LAT,$MAIN_LON,30,0 &
    # screen -dm -S jmavsim JMAVSim.sh start &
    screen -dm -S simvehicle SimVehicle.sh start &
    sleep 10

    # =========================================================================
    # Communications: MavProxy
    # =========================================================================

    # screen -dm -S mavproxy mavproxy.py --master=tcp:127.0.0.1:5760 --out=udpout:127.0.0.1:14550 --out=udpout:127.0.0.1:14560
    # screen -dm -S mavproxy.py --master=udp:127.0.0.1:14550 --out=udpout:127.0.0.1:14570 --out=udpout:127.0.0.1:14580
    # None
    # sleep 10
    
    # =========================================================================
    # Ground Control Stations: QGroundControl
    # =========================================================================
   
    QGroundControl.sh start &
    sleep 10

    # =========================================================================
    # Global Positioning System
    # =========================================================================

    sudo service gpsd stop
    sleep 3
    cd $GPS_DIRECTORY
    gpsfake -c 1 FakeGpsData.log
    sleep 3
    # python FollowMe.py --connect "127.0.0.1:14551"
    
elif [ "$GPS_ARGUMENT_ACTION" = "stop" ]; then
    
    QGroundControl.sh stop
    sleep 1
    SimVehicle.sh stop
    sleep 1
    GPS_PID=`cat $GPS_PID_PATH`
    kill -- -$(ps -o pgid=$GPS_PID | grep -o [0-9]*)
    
fi

cd $HOME

# End Of File

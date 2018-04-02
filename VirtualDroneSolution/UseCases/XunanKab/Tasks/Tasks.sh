#!/bin/bash

TASK=$1

COUNTER=2
while [  $COUNTER -lt 5 ]; do
    echo The counter is $COUNTER
    RANDOMLAT=`echo $((1 + RANDOM % 100))`
    RANDOMLON=`echo $((1 + RANDOM % 100))`
    if [ "$TASK" = "telemetry" ]; then
        python Telemetry.py --connect=tcp:172.17.0.${COUNTER}:5763 &
    elif [ "$TASK" = "goto" ]; then
        python GoTo.py --connect=tcp:172.17.0.${COUNTER}:5763 --lat=20.65${RANDOMLAT}009 --long=-103.39${RANDOM}602 --alt=5 &
    elif [ "$TASK" = "random" ]; then
        python GoTo.py --connect=tcp:172.17.0.2:5763 --lat=20.65${RANDOMLAT}009 --long=-103.39${RANDOM}602 --alt=5 &
        python Triangle.py --connect=tcp:172.17.0.3:5763 &
        python Square.py --connect=tcp:172.17.0.4:5763 &
    elif [ "$TASK" = "follow" ]; then
    fi
        python Square.py --connect=tcp:172.17.0.2:5763 &
        sleep 5
        python Square.py --connect=tcp:172.17.0.3:5763 &
        sleep 5
        python Square.py --connect=tcp:172.17.0.4:5763 &
    fi
    let COUNTER=COUNTER+1
done


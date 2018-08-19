#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# Libraries
# =============================================================================

import argparse
import json
import math
import sys
import time

import paho.mqtt.client as paho

from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil

from dronekit import connect, Command, LocationGlobal, VehicleMode, LocationGlobalRelative

from threading import Thread

# =============================================================================
# Functions
# =============================================================================

def battery_callback(self, attr_name, value):
    print(vehicle.battery)
    print(str(vehicle.battery))
    client = paho.Client()
    client.connect("iot.eclipse.org", 1883, 60)
    topic = "xunankab/quintanaroo/battery"
    #client.publish(topic, payload=json.dumps(vehicle.battery))

def heading_callback(self, attr_name, value):
    payload = {}
    payload["heading"] = vehicle.heading
    client = paho.Client()
    client.connect("iot.eclipse.org", 1883, 60)
    topic = "xunankab/quintanaroo/heading"
    client.publish(topic, json.dumps(payload))

def wildcard_callback(self, attr_name, value):
    print " CALLBACK: (%s): %s" % (attr_name,value)

# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':

    # Set up option parsing to get connection string
    parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
    parser.add_argument('--connect',
                        help="Vehicle connection target string. If not specified, SITL automatically started and used.")
    parser.add_argument('--id')
    args = parser.parse_args()

    connection_string = args.connect
    vehicleid = float(args.id)
    sitl = None

    # Start SITL if no connection string specified
    if not connection_string:
        import dronekit_sitl
        sitl = dronekit_sitl.start_default()
        connection_string = sitl.connection_string()

    # Connect to the Vehicle
    print('Connecting to vehicle on: %s' % connection_string)
    vehicle = connect(connection_string, wait_ready=True)

    vehicle.parameters['SYSID_THISMAV'] = vehicleid
    print " Type: %s" % vehicle._vehicle_type
    print " Armed: %s" % vehicle.armed
    print " System status: %s" % vehicle.system_status.state
    print " GPS: %s" % vehicle.gps_0
    print " Alt: %s" % vehicle.location.global_relative_frame.alt

    vehicle.add_attribute_listener('battery', battery_callback)
    vehicle.add_attribute_listener('heading', heading_callback)
    #vehicle.add_attribute_listener('*', wildcard_callback)

    time.sleep(5)

    vehicle.remove_attribute_listener('battery', battery_callback)
    #vehicle.remove_attribute_listener('*', wildcard_callback)


    # Close vehicle object
    vehicle.close()

    # Shut down simulator if it was started.
    if sitl:
        sitl.stop()

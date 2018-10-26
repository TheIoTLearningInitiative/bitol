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
from ppretty import ppretty
from pymavlink import mavutil

from dronekit import connect, Command, LocationGlobal, VehicleMode, LocationGlobalRelative

from threading import Thread

# =============================================================================
# Functions
# https://github.com/xe1gyq/Team0UavProject
# =============================================================================

def system_status_callback(self, attr_name, value):
    topic = "xunankab/quintanaroo/connectivity"
    if vehicle.system_status.state == "ACTIVE":
        payload["status"] = "ON"
    else:
        payload["status"] = "OFF"
    client.publish(topic, payload=json.dumps(payload))

def battery_callback(self, attr_name, value):
    topic = "xunankab/quintanaroo/battery"
    payload["battery"] = vehicle.battery.voltage
    client.publish(topic, payload=json.dumps(payload))

def heading_callback(self, attr_name, value):
    topic = "xunankab/quintanaroo/heading"
    payload["heading"] = vehicle.heading
    client.publish(topic, payload=json.dumps(payload))

def location_callback(self, attr_name, value):
    topic = "xunankab/quintanaroo/altitude"
    payload["altitude"] = vehicle.location.global_relative_frame.alt
    client.publish(topic, payload=json.dumps(payload))

def wildcard_callback(self, attr_name, value):
    print " CALLBACK: (%s): %s" % (attr_name,value)
    topic = "xunankab/quintanaroo"
    client.publish(topic, payload=json.dumps(payload))

# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
    parser.add_argument('--connect',
                        help="Vehicle connection target string. If not specified, SITL automatically started and used.")
    parser.add_argument('--id')
    args = parser.parse_args()

    connection_string = args.connect
    vehicleid = float(args.id)
    sitl = None

    client = paho.Client()
    client.connect("iot.eclipse.org", 1883, 60)

    payload = {}

    if not connection_string:
        import dronekit_sitl
        sitl = dronekit_sitl.start_default()
        connection_string = sitl.connection_string()

    print('Connecting to vehicle on: %s' % connection_string)
    vehicle = connect(connection_string, wait_ready=True)

    vehicle.parameters['SYSID_THISMAV'] = vehicleid
    print " Type: %s" % vehicle._vehicle_type
    print " Armed: %s" % vehicle.armed
    print " System status: %s" % vehicle.system_status.state
    print " GPS: %s" % vehicle.gps_0
    print " Alt: %s" % vehicle.location.global_relative_frame.alt

    vehicle.add_attribute_listener('system_status', system_status_callback)
    vehicle.add_attribute_listener('battery', battery_callback)
    vehicle.add_attribute_listener('heading', heading_callback)
    vehicle.add_attribute_listener('location', location_callback)
    #vehicle.add_attribute_listener('*', wildcard_callback)

    time.sleep(120)

    vehicle.remove_attribute_listener('location', location_callback)
    vehicle.remove_attribute_listener('heading', heading_callback)
    vehicle.remove_attribute_listener('battery', battery_callback)
    vehicle.remove_attribute_listener('system_status', system_status_callback)
    #vehicle.remove_attribute_listener('*', wildcard_callback)

    vehicle.close()

    if sitl:
        sitl.stop()
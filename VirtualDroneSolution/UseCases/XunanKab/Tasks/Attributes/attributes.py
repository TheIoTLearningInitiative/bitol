#!/usr/bin/python

# =============================================================================
# Libraries
# =============================================================================

# Set up option parsing to get connection string
import argparse

# Import DroneKit-Python
from dronekit import connect, VehicleMode

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Print out vehicle state information. Connects to SITL on local PC by default.')
    parser.add_argument('--connect',
                       help="vehicle connection target string. If not specified, SITL automatically started and used.")
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

    # Connect to the Vehicle.
    #   Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.
    print "\nConnecting to vehicle on: %s" % connection_string
    vehicle = connect(connection_string, wait_ready=True)

    vehicle.parameters['SYSID_THISMAV'] = vehicleid
    # Get some vehicle attributes (state)
    print "Get some vehicle attribute values:"
    print " Autopilot Firmware version: %s" % vehicle.version
    #print " Autopilot capabilities (supports ftp): %s" % vehicle.capabilities.ftp
    print " Global Location: %s" % vehicle.location.global_frame
    print " Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
    print " Local Location: %s" % vehicle.location.local_frame
    print " Attitude: %s" % vehicle.attitude
    print " Velocity: %s" % vehicle.velocity
    print " GPS: %s" % vehicle.gps_0
    print " Groundspeed: %s" % vehicle.groundspeed
    print " Airspeed: %s" % vehicle.airspeed
    print " Gimbal status: %s" % vehicle.gimbal
    print " Battery: %s" % vehicle.battery
    print " EKF OK?: %s" % vehicle.ekf_ok
    print " Last Heartbeat: %s" % vehicle.last_heartbeat
    print " Rangefinder: %s" % vehicle.rangefinder
    print " Rangefinder distance: %s" % vehicle.rangefinder.distance
    print " Rangefinder voltage: %s" % vehicle.rangefinder.voltage
    print " Heading: %s" % vehicle.heading
    print " Armed: %s" % vehicle.armed
    print " Is Armable?: %s" % vehicle.is_armable
    print " System status: %s" % vehicle.system_status.state
    print " Mode: %s" % vehicle.mode.name

    # Close vehicle object before exiting script
    vehicle.close()

    print("Completed")

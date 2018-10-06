import time
from dronekit import connect, VehicleMode
#import modules.UDPserver as udp
from modules.utils import *
from modules.pixVehicle import *

# Connection to the vehicle
# SITL via TCP
#vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True)
# SITL/vehicle via UDP (connection coming from mavproxy.py)
vehicle = connect('tcp:172.17.0.3:5763', wait_ready=True)
# Direct UART communication to Pixhawk
#vehicle = connect('/dev/ttyAMA0', wait_ready=True)

""" Mission starts here """

print "\n\nAttempting to start take off!!\n\n"
arm_and_takeoff(vehicle, 10)
print "Wait 5 seconds before going landing"
print "Current altitude: ", vehicle.location.global_relative_frame.alt
time.sleep(5)
print "\n\nLanding!\n\n"
#vehicle.mode = VehicleMode("RTL")
vehicle.mode = VehicleMode("LAND")

while vehicle.armed:
    print "Current altitude: ", vehicle.location.global_relative_frame.alt
    time.sleep(0.5)

print "\n\nMission complete\n\n"
vehicle.close()

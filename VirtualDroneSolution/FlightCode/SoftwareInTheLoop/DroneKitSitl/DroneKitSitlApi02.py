import time

from dronekit_sitl import SITL
from dronekit_sitl import version_list

copter_args = ['-S', '--model', 'quad', '--home=-20.6207591,-103.3991668,584,353']

versions = version_list()
print versions.keys()

sitl = SITL()
sitl.download('copter', '3.3')
sitl.launch(copter_args, verbose=True, await_ready=True, use_saved_data=False)
time.sleep(5)
sitl.stop()

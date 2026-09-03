from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait, StopWatch

from robot_config import create_robot


# Get the hub, wheels, and shared driving settings from robot_config.py.
hub, drive_base, left_motor, right_motor = create_robot()

# Each list shows the number of teeth on two gears that touch each other.
# The complete gear train slows each attachment motor by a 3-to-1 ratio.
attachment_left = Motor(Port.C, gears=[[20, 12], [12, 36], [12, 20]])
attachment_right = Motor(Port.B, gears=[[20, 12], [12, 36], [12, 20]])

# Optional setup: move each arm to its hard stop and call that angle 0 degrees.
# A speed of -200 degrees per second moves the arm toward its hard stop.
# A 30 percent power limit helps protect the gears.
# attachment_left.run_until_stalled(-200, then=Stop.HOLD, duty_limit=30)
# attachment_left.reset_angle(0)
# attachment_right.run_until_stalled(-200, then=Stop.HOLD, duty_limit=30)
# attachment_right.reset_angle(0)

# Let the robot sit still so the gyro can get ready.
# Stop waiting after 2,000 milliseconds, which is the same as 2 seconds.
settle_timer = StopWatch()
while not hub.imu.stationary() and settle_timer.time() < 2000:
    # Wait 10 milliseconds before checking the gyro again.
    wait(10)

# Optional setup: drive backward 10 millimeters to take up loose space in the gears.
# Then reset the traveled distance to 0 millimeters and the heading to 0 degrees.
# drive_base.straight(-10)
# drive_base.reset()

# Optional setup: raise each arm to an angle of 90 degrees.
# Move each arm at 300 degrees per second, a safe speed for the 3-to-1 gears.
# attachment_left.run_target(speed=300, target_angle=90, wait=False)
# attachment_right.run_target(speed=300, target_angle=90, wait=False)

# Drive forward 80 millimeters, and then drive backward 80 millimeters.
drive_base.straight(80)
drive_base.straight(-80)

# Turn off power to the wheel motors when the mission is finished.
drive_base.stop()

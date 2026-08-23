from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# Hub and drive motors.
hub = PrimeHub()
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E, Direction.CLOCKWISE)

# Attachment motors. Gear list reads from the motor outward and works out to 3 to 1.
# If the two mechanisms are mirrored, one of these needs Direction.COUNTERCLOCKWISE.
attachment_left = Motor(Port.C, gears=[[20, 12], [12, 36], [12, 20]])
attachment_right = Motor(Port.B, gears=[[20, 12], [12, 36], [12, 20]])

# Find each hard stop and call it zero. duty_limit keeps the gears from stripping.
attachment_left.run_until_stalled(-200, then=Stop.HOLD, duty_limit=30)
attachment_left.reset_angle(0)
attachment_right.run_until_stalled(-200, then=Stop.HOLD, duty_limit=30)
attachment_right.reset_angle(0)

# Robot measurements in mm.
WHEEL_DIAMETER = 56
AXLE_TRACK = 164

drive_base = DriveBase(left_motor, right_motor, wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)

# Gyro on before the reset, so the reset also zeros the gyro.
drive_base.use_gyro(True)

# Fixed speeds so every run behaves the same.
drive_base.settings(straight_speed=300, straight_acceleration=600, turn_rate=200, turn_acceleration=400)


# Let the robot settle so the gyro zeros cleanly. Give up after 2 seconds.
settle_timer = StopWatch()
while not hub.imu.stationary() and settle_timer.time() < 2000:
    wait(10)

# Small nudge back to take up slack in the gears. Resets distance, heading, and gyro in one call.
drive_base.straight(-10)
drive_base.reset()

# Raise both arms to the start pose. 300 is the safe ceiling at 3 to 1 gearing.

#attachment_left.run_target(speed=300, target_angle=90, wait=False)
#attachment_right.run_target(speed=300, target_angle=90, wait=False)

# Write your code.
#drive_base.straight(100)
#drive_base.straight(-100)
drive_base.stop()
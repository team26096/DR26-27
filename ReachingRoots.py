from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase


# Initialize the hub
hub = PrimeHub()

# Drive motors setup
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E, Direction.CLOCKWISE)

# Attachment motors setup
# 1:1 bevel gear ratio means 1 degree of motor rotation = 1 degree of arm movement
attachment_right = Motor(Port.C, gears=[[12,20],[12,12]])
attachment_left = Motor(Port.B, gears=[[12,20],[12,12]])


# DriveBase setup
WHEEL_DIAMETER = 62.4
AXLE_TRACK = 164

drive_base = DriveBase(left_motor, right_motor, wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)
drive_base.use_gyro(True)

# left_motor.reset_angle(0)
hub.imu.reset_heading(0)

drive_base.reset()


#attachment_right.run_until_stalled(-200, then=Stop.HOLD, duty_limit=30)
#attachment_right.reset_angle(0)
attachment_right.run_angle(speed=650, rotation_angle=210)
#drive_base.straight(-10)
drive_base.reset()
drive_base.straight(865)
drive_base.turn(15)
attachment_right.run_angle(speed=650, rotation_angle=-120)
attachment_right.run_angle(speed=650, rotation_angle=120)

# Go all the way backwards (slower) to align with back walls - 3cm (-30mm)
drive_base.settings(straight_speed=200)
drive_base.straight(-30)

drive_base.turn(-42)

# drive_base.turn(-22)
attachment_right.run_angle(speed=650, rotation_angle=-100)
attachment_left.run_angle(speed=650, rotation_angle=100)

drive_base.straight(50)

attachment_left.run_angle(speed=650, rotation_angle=-90)

drive_base.stop()
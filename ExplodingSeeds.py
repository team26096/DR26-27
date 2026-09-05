
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

watch = StopWatch()

# Initialize the hub
hub = PrimeHub()

# Drive motors setup
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E, Direction.CLOCKWISE)

# Attachment motors setup
# 1:1 bevel gear ratio means 1 degree of motor rotation = 1 degree of arm movement
attachment_right = Motor(Port.C, gears=[[12,20],[12,20]])
attachment_left = Motor(Port.B, gears=[[12,20],[12,20]])



# DriveBase setup
WHEEL_DIAMETER = 62.4
AXLE_TRACK = 164

drive_base = DriveBase(left_motor, right_motor, wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)
drive_base.use_gyro(True)

# left_motor.reset_angle(0)
hub.imu.reset_heading(0)

drive_base.reset()

# --- Right Attachment Motor Actions (Port C) ---

drive_base.settings(straight_speed=600)
drive_base.straight(200)

drive_base.turn(50)

drive_base.settings(straight_speed=400)
drive_base.straight(330)

attachment_right.run_angle(speed=200, rotation_angle=20)

# drive_base.straight(-12)

drive_base.settings(straight_speed=100)

attachment_right.run_angle(speed=50, rotation_angle=5)
drive_base.straight(-18)
# drive_base.straight(-10)
attachment_right.run_angle(speed=25, rotation_angle=10)
drive_base.straight(-15)
attachment_right.run_angle(speed=30, rotation_angle=30)

drive_base.settings(straight_speed=500)

drive_base.straight(-60)

drive_base.straight(-360)
 

# wait(1000)

timestamp = watch.time()/1000
print("Timestamp:", timestamp)


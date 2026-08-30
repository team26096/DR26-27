
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait

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

# --- Right Attachment Motor Actions (Port C) ---

# Go forward to start aligning with exploding seeds
drive_base.settings(straight_speed=300)
drive_base.straight(250)

drive_base.turn(45)

# Go forward to align with exploding seeds
drive_base.settings(straight_speed=200)
drive_base.straight(270)

# 1. Lower Port  arm 80 degrees at speed 200
attachment_right.run_angle(speed=150, rotation_angle=-150)

wait(1000)

# Go backwards (slower) to align with back walls - 80cm (-80mm)
drive_base.settings(straight_speed=100)
drive_base.straight(-100)

wait(1000)
 
# 1. Lift Port A arm 150 degrees at speed 200
attachment_right.run_angle(speed=150, rotation_angle=150)
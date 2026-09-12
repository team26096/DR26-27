
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ForceSensor, Motor
from pybricks.parameters import Port, Direction, Stop
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
attachment_left = Motor(Port.B, gears=[[12,20],[12,36]])



# DriveBase setup
WHEEL_DIAMETER = 62.4
AXLE_TRACK = 164

drive_base = DriveBase(left_motor, right_motor, wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)
drive_base.use_gyro(True)

# left_motor.reset_angle(0)
hub.imu.reset_heading(0)

drive_base.reset()

# --- Right Attachment Motor Actions (Port C) ---


# Drive forward from base to start aligning with exploding seeds 
drive_base.settings(straight_speed=600)
drive_base.straight(200, wait=False)

# Lift arm until stalled to set up for Biocentric Architecture
attachment_left.run_until_stalled(-170, then=Stop.HOLD, duty_limit=35)


# Turn robot to continue aligning with exploding seeds
drive_base.turn(50)

# Go forward to make contact with seed in exploding seeds
drive_base.settings(straight_speed=400)
drive_base.straight(320)

# Lift arm to align for seed removal
attachment_right.run_angle(speed=200, rotation_angle=20)

drive_base.settings(straight_speed=100)

# Three movements for lifting the arm slightly and moving back to get the arms out and get the seed out  
attachment_right.run_angle(speed=50, rotation_angle=5)
drive_base.straight(-18)
attachment_right.run_angle(speed=25, rotation_angle=5)
drive_base.straight(-15)
attachment_right.run_angle(speed=10, rotation_angle=22)

drive_base.settings(straight_speed=100)

# Move backward to get clear of exploding seeds to prepare for Biocentric Architecture
drive_base.straight(-200)

# Turn to get into posistion to move forward to Biocentric Architecture
drive_base.turn(33)

drive_base.settings(straight_speed=500)

# Move arm down to prepare for tasks in Biocentric Architecture
attachment_left.run_angle(speed=200, rotation_angle=163, wait=False)

# Move forward lots in preperation for Biocentric Architecture
drive_base.straight(620)

drive_base.settings(straight_speed=100)

# Turn left slightlyto align with Biocentric Architecture
drive_base.turn(-17)

# Move arm down 20 degrees to complete compost hatch in Biocentric Architecture
attachment_left.run_angle(speed=100, rotation_angle=20)

# Move arm up 45 degrees to complete nesting canopy in Biocentric Architecture
attachment_left.run_angle(speed=25, rotation_angle=-45)

# Again move arm down to safely and make sure compost hatch is complete
attachment_left.run_angle(speed=100, rotation_angle=50)

drive_base.settings(straight_speed=250)

# Turn right to move away from Biocentric Architecture
drive_base.turn(20)

# Move forward to start aligning with window to the past seed
drive_base.straight(120)

# Turn left to align with window to the past seed in preperation for seed removal
drive_base.turn(-30)

# Move right arm down 40 degrees to align arm for seed removal from window to the past
attachment_right.run_angle(speed=100, rotation_angle=-40)

# Move forward so the right attachment arm is under the seed and ready for pickup
drive_base.straight(130)

# Move arm up 60 degrees to pick up the seed from window to the past
attachment_right.run_angle(speed=100, rotation_angle=60)

timestamp = watch.time()/1000
print("Timestamp:", timestamp)


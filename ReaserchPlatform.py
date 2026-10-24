
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
AXLE_TRACK = 151

drive_base = DriveBase(left_motor, right_motor, wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)
drive_base.use_gyro(True)

drive_base.settings(straight_speed=600, straight_acceleration=200,
                    turn_rate=200, turn_acceleration=200)

# left_motor.reset_angle(0)
hub.imu.reset_heading(0)

drive_base.reset()
drive_base.straight(570)
drive_base.arc(10,90)
drive_base.straight(190) 
drive_base.arc(-82, angle=90)
drive_base.straight(150)   
attachment_right.run_angle(speed=600, rotation_angle=45, then=Stop.HOLD)
drive_base.straight(-150) 
attachment_right.run_angle(speed=600, rotation_angle=-45, then=Stop.HOLD)
drive_base.stop()

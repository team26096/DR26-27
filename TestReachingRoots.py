from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase

# Initialize the hub
hub = PrimeHub()

# Drive motors setup
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E, Direction.CLOCKWISE)

# Attachment motors setup
# 1:1 bevel gear ratio means 1 degree of motor rotation = 1 degree of arm movement
attachment_right = Motor(Port.C)
attachment_left = Motor(Port.B)

# DriveBase setup
WHEEL_DIAMETER = 56
AXLE_TRACK = 164

drive_base = DriveBase(left_motor, right_motor, wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)
drive_base.use_gyro(True)

left_motor.reset_angle(0)
right_motor.reset_angle(0)

hub.imu.reset_heading(0)

drive_base.reset()

# --- Right Attachment Motor Actions (Port B) ---

# 1. Lift Port C arm 170 degrees at speed 75
attachment_right.run_angle(speed=125, rotation_angle=170)



# straight() already stops and holds at the end, so this line is optional.
# stop() lets the motors coast, which makes the robot easy to lift out
# but also easy to knock out of place.
# Use brake() instead if you want it to stay planted.
drive_base.stop()

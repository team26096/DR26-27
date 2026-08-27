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
attachment_right = Motor(Port.B, gears=[[12,20],[12,12]])
attachment_left = Motor(Port.C, gears=[[12,20],[12,12]])



# DriveBase setup
WHEEL_DIAMETER = 56
AXLE_TRACK = 164

drive_base = DriveBase(left_motor, right_motor, wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)
drive_base.use_gyro(True)

# left_motor.reset_angle(0)
hub.imu.reset_heading(0)

drive_base.reset()

# --- Right Attachment Motor Actions (Port C) ---

# 3. Drive forward 670 mm in a straight line using gyro stabilization
# drive_base.straight(670, wait=True)



# 1. Lower Port  arm 80 degrees at speed 200
# attachment_right.run_angle(speed=200, rotation_angle=45)

# Go all the way backwards (slower) to align with back walls - 3cm (-30mm)
# drive_base.settings(straight_speed=200)

# Lower arm Port B arm 20 degrees at speed 75
# attachment_right.run_angle(speed=250, rotation_angle=-45)
# drive_base.straight(-40)
#drive_base.straight(40)
# 3. Drive forward 50 mm in a straight line using gyro stabilization
# drive_base.straight(50)

# Lift Port B arm 20 degrees at speed 75
#attachment_right.run_angle(speed=550, rotation_angle=200)

# Go all the way backwards (slower) to align with back walls - 3cm (-30mm)
# drive_base.settings(straight_speed=200)
# drive_base.straight(-30)

# Lower arm Port B arm 20 degrees at speed 75
#attachment_right.run_angle(speed=250, rotation_angle=-200)

# # 3. Drive forward 50 mm in a straight line using gyro stabilization
# drive_base.straight(50)

# # Lift Port B arm 20 degrees at speed 75
# attachment_right.run_angle(speed=550, rotation_angle=200)

# straight() already stops and holds at the end, so this line is optional.
# stop() lets the motors coast, which makes the robot easy to lift out
# but also easy to knock out of place.
# Use brake() instead if you want it to stay planted.

# Lift Port B arm 20 degrees at speed 75
attachment_right.run_angle(speed=650, rotation_angle=-110)

# Lower arm Port  arm 20 degrees at speed 75
attachment_right.run_angle(speed=650, rotation_angle=-30)



drive_base.stop()
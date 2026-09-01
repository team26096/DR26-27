# to load this code from terminal use the following command
# py -3 -m pybricksdev run ble .\run1.py --no-start --name pixiebricks

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch
import sys

timer = StopWatch()

hub = PrimeHub()

# Drive motors
left_drive = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_drive = Motor(Port.E, Direction.CLOCKWISE)
drivebase = DriveBase(
    left_drive,
    right_drive,
    wheel_diameter=62.4,
    axle_track=164
)
drivebase.use_gyro(True)
current_settings = drivebase.settings()
print("Robot Settings:", current_settings)
print("Robot max",drivebase.distance_control.limits())

# Attachment motor
left_attach = Motor(
    Port.B,
    gears=[
        [12, 20],
        [12, 12],
    ]
)

right_attach = Motor(
    Port.C,
    gears=[
        [12, 20],
        [12, 36],
    ]
)

print("Attachment motor max:", left_attach.control.limits())

# drivebase.settings(100,100,125,500)
# Drive - drivebase.straight()
# Turn - drivebase.turn()
# Attachment - left_attach.run_angle(speed=360, rotation_angle=55, then=Stop.HOLD, wait=True)
# Attachment - right_attach.run_angle(speed=360, rotation_angle=55, then=Stop.HOLD, wait=True)

# Humoungous Fungus

# Move attachment motor upward until it stalls
left_attach.run_until_stalled(
    -500,          # speed in deg/s; use -500 if this is the wrong direction
    then=Stop.HOLD,
    duty_limit=30
)

# Make this stalled position the new zero
left_attach.reset_angle(0)
print(left_attach.angle())
left_attach.run_angle(speed=200, rotation_angle=130, then=Stop.HOLD, wait=False)
drivebase.straight(750)
left_attach.run_angle(speed=400, rotation_angle=-90, then=Stop.HOLD, wait=True)
print(left_attach.angle())

# #Forest Elder
drivebase.turn(90)
left_attach.run_angle(speed=200, rotation_angle=120, then=Stop.HOLD, wait=True)
print(left_attach.angle())
drivebase.straight(80)
left_attach.run_angle(speed=200, rotation_angle=-45, then=Stop.HOLD, wait=True)

elapsed_seconds = timer.time() / 1000
print("Elapsed time: {:.2f} seconds".format(elapsed_seconds))

#Go backward to knock down window to the past
drivebase.straight(-300)

drivebase.turn(64)

drivebase.straight(210)

drivebase.turn(25)
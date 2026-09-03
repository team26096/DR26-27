# to execute this code from terminal use the following command
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
        [12, 12],
        [12, 12],
    ]
)

right_attach = Motor(
    Port.C,
    gears=[
        [12, 12],
        [12, 12],
    ]
)

drivebase.straight(400)

drivebase.turn(28)

drivebase.straight(60)

drivebase.straight(43)

drivebase.turn(10)




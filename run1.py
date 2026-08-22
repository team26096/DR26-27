# to execute this code from terminal use the following command
# py -3 -m pybricksdev run ble .\run1.py --no-start --name pixiebricks

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase
import sys

hub = PrimeHub()

# Drive motors
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E, Direction.CLOCKWISE)

# Attachment motor
motor_c = Motor(
    Port.C,
    gears=[
        [20, 12],
        [12, 36],
        [12, 20]
    ]
)

drivebase = DriveBase(
    left_motor,
    right_motor,
    wheel_diameter=62.4,
    axle_track=164
)

drivebase.use_gyro(True)

current_settings = drivebase.settings()
print("Robot Settings:", current_settings)

# Drive forward 55 cm
drivebase.straight(500)
drivebase.settings(20,100,125,500)
drivebase.straight(100)

#drivebase.turn(-93)

motor_c.run_angle(
    speed=360,
    rotation_angle=55,
    then=Stop.HOLD,
    wait=True
)

motor_c.run_angle(
    speed=360,
    rotation_angle=-75,
    then=Stop.HOLD,
    wait=True
)

# Drive forward Backward10 cm
# drivebase.straight(-480)


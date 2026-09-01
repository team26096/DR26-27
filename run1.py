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
        [12, 36],
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
#left_attach.reset_angle(0)
#print(left_attach.angle())
#left_attach.run_angle(speed=1030, rotation_angle=-26.5, then=Stop.HOLD, wait=False)
#drivebase.straight(750)
#left_attach.run_angle(speed=1030, rotation_angle=-90, then=Stop.HOLD, wait=True)
#print(left_attach.angle())
#Forest Elder

#drivebase.turn(90)
#left_attach.run_angle(speed=1030, rotation_angle=116, then=Stop.HOLD, wait=True)
#print(left_attach.angle())
#drivebase.straight(80)
#left_attach.run_angle(speed=1030, rotation_angle=-45, then=Stop.HOLD, wait=True)

elapsed_seconds = timer.time() / 1000
print("Elapsed time: {:.2f} seconds".format(elapsed_seconds))

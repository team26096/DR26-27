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
    axle_track=151 #164
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
        [20, 20],
    ]
)

right_attach = Motor(
    Port.C,
    gears=[
        [12, 20],
        [1, 24],
    ]
)

print("Attachment motor max:", left_attach.control.limits())

drivebase.settings(500,(800,400),125,500)
drivebase.straight(-5)

# Drive - drivebase.straight()
# Turn - drivebase.turn()
# Attachment - left_attach.run_angle(speed=360, rotation_angle=55, then=Stop.HOLD, wait=True)
# Attachment - right_attach.run_angle(speed=360, rotation_angle=55, then=Stop.HOLD, wait=True)

# Humoungous Fungus

# Move attachment motor upward until it stalls
left_attach.run_until_stalled(
    -500,          # speed in deg/s; use -500 if this is the wrong direction
    then=Stop.HOLD,
    duty_limit=25
)

# Make this stalled position the new zero
left_attach.reset_angle(0)
# Move arm down to correct angle for humongous fungus
left_attach.run_angle(speed=360, rotation_angle=120,then=Stop.HOLD, wait=True)
# go straight to humungous fungs
drivebase.straight(770)
# flick fungus up
left_attach.run_angle(speed=600, rotation_angle=-90, then=Stop.HOLD, wait=True)
print(left_attach.angle())
# go back from humungus fungus
drivebase.straight(-40)
#turn to keystone speices
drivebase.turn(50)
drivebase.straight(160)
# drop keystone speices
right_attach.run_angle(speed=360, rotation_angle=80, then=Stop.HOLD, wait=True)
right_attach.run_angle(speed=360, rotation_angle=-30, then=Stop.HOLD, wait=False)
# go back from keystone speices
drivebase.straight(-120)
# Turn to setup for Forest Elder
drivebase.turn(40)
# move arm back down for forest elder
left_attach.run_angle(speed=200, rotation_angle=120, then=Stop.HOLD, wait=True)
print(left_attach.angle())
# move front and then flick support for forest elder up
drivebase.straight(90)
left_attach.run_angle(speed=400, rotation_angle=-45, then=Stop.HOLD, wait=True)

drivebase.arc(75.5, angle=-90)
drivebase.straight(-650)

elapsed_seconds = timer.time() / 1000
print("Elapsed time: {:.2f} seconds".format(elapsed_seconds))

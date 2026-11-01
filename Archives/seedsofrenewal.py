# to execute this code from terminal use the following command
# py -3 -m pybricksdev run ble .\run1.py --no-start --name pixiebricks

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
import sys

hub = PrimeHub()

voltage = hub.battery.voltage()
print("Battery Voltage:", voltage, "mV")

# Drive motors
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E, Direction.CLOCKWISE)

# Attachment motor
motor_right  = Motor(
    Port.C,
    gears=[
        [12, 36]
    ]
)



drivebase = DriveBase(
    left_motor,
    right_motor,
    wheel_diameter=62.4,
    axle_track=160
)

drivebase.use_gyro(True)

# Make straight driving faster
drivebase.settings(
    straight_speed=500,         # mm/s
    straight_acceleration=400  # mm/s^2
)

current_settings = drivebase.settings()
print("Robot Settings:", current_settings)

# TIMER START. A StopWatch counts from the moment it is created.
run_timer = StopWatch()
drivebase.straight(330)
motor_right.run_angle(
    speed=90,
    rotation_angle=90,
    then=Stop.HOLD,
    wait=True
)
# # TIMER STOP. pause() freezes the value so it cannot creep up after this line.
run_timer.pause()

# # time() returns milliseconds, so divide by 1000 to get seconds.
elapsed = round(run_timer.time() / 1000, 1)
print("Total run time:", elapsed, "seconds")
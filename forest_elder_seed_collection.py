# to execute this code from terminal use the following command
# py -3 -m pybricksdev run ble .\run1.py --no-start --name pixiebricks

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
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

motor_left = Motor(
    Port.B,
    gears=[
        [12, 20],
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

# Make straight driving faster
drivebase.settings(
    straight_speed=500,         # mm/s
    straight_acceleration=400  # mm/s^2
)

current_settings = drivebase.settings()
print("Robot Settings:", current_settings)



# TIMER START. A StopWatch counts from the moment it is created.
run_timer = StopWatch()


motor_c.run_until_stalled(200, then=Stop.HOLD, duty_limit=25 )
motor_left.run_until_stalled(200, then=Stop.HOLD, duty_limit=25 )
motor_left.reset_angle(0)
motor_left.run_angle(
    speed=200,
    rotation_angle=-45,
    then=Stop.HOLD,
    wait=True
)

# 1. Drive forward 50 cm = 500 mm
drivebase.straight(410)

# 2. Rotate the entire robot 30 degrees
drivebase.turn(37)


drivebase.straight(112)

motor_left.run_angle(
    speed=90,
    rotation_angle=35,
    then=Stop.HOLD,
    wait=True
)



# # 4. Rotate Motor C 45 degrees2
motor_c.run_angle(
    speed=200,
    rotation_angle=-55,
    then=Stop.HOLD,
    wait=True
)

drivebase.straight(-160)

motor_c.run_angle(
    speed=200,
    rotation_angle=30,
    then=Stop.HOLD,
    wait=True
)

drivebase.straight(-120)
drivebase.turn(-12)
# drivebase.straight(-25)
drivebase.turn(-80)
drivebase.straight(-350)
# drivebase.stop()


# ---------- RESULT ----------

# # TIMER STOP. pause() freezes the value so it cannot creep up after this line.
run_timer.pause()

# # time() returns milliseconds, so divide by 1000 to get seconds.
elapsed = round(run_timer.time() / 1000, 1)
print("Total run time:", elapsed, "seconds")


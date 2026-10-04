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
    straight_acceleration=816  # mm/s^2
)

current_settings = drivebase.settings()
print("Robot Settings:", current_settings)



# TIMER START. A StopWatch counts from the moment it is created.
run_timer = StopWatch()


motor_c.run_until_stalled(200, then=Stop.HOLD, duty_limit=25 )

# 1. Drive forward 50 cm = 500 mm
drivebase.straight(410)

# 2. Rotate the entire robot 30 degrees
drivebase.turn(42)

# 3.Drive forward 50 mm
drivebase.straight(130)

# 4. Rotate Motor C 45 degrees
motor_c.run_angle(
    speed=300,
    rotation_angle=-48,
    then=Stop.HOLD,
    wait=True
)

drivebase.straight(-115)

motor_c.run_angle(
    speed=400,
    rotation_angle=30,
    then=Stop.HOLD,
    wait=True
)

#drivebase.turn(-25)

drivebase.straight(-120)
drivebase.turn(-12)

motor_c.run_angle(
    speed=400,
    rotation_angle=-30,
    then=Stop.HOLD,
    wait=True
)
motor_left.run_until_stalled(200, then=Stop.HOLD, duty_limit=25 )
motor_left.reset_angle(0)
# 1. Drive forward 50 cm = 500 mm

motor_left.run_angle(
    speed=200,
    rotation_angle=-45,
    then=Stop.HOLD,
    wait=True
)
drivebase.straight(235)
motor_left.run_angle(
    speed=90,
    rotation_angle=35,
    then=Stop.HOLD,
    wait=True
)
drivebase.straight(-25)
drivebase.stop()


# ---------- RESULT ----------

# TIMER STOP. pause() freezes the value so it cannot creep up after this line.
run_timer.pause()

# time() returns milliseconds, so divide by 1000 to get seconds.
elapsed = round(run_timer.time() / 1000, 1)
print("Total run time:", elapsed, "seconds")

# Scrolls about one second per character. Delete if it gets in the way.
hub.display.text(str(elapsed))

# # # Drive forward 55 cm
# # drivebase.straight(500)
# # drivebase.settings(20,100,125,500)
# # drivebase.straight(100)

# # #drivebase.turn(-93)

# # motor_c.run_angle(
# #     speed=360,
# #     rotation_angle=55,
# #     then=Stop.HOLD,
# #     wait=True
# # )

# # motor_c.run_angle(
# #     speed=360,
# #     rotation_angle=-75,
# #     then=Stop.HOLD,
# #     wait=True
# # )

# # # Drive forward Backward10 cm
# # # drivebase.straight(-480)


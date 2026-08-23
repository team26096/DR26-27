from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# Hub and drive motors.
hub = PrimeHub()
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E, Direction.CLOCKWISE)

# Robot measurements in mm.
WHEEL_DIAMETER = 56
AXLE_TRACK = 164

drive_base = DriveBase(left_motor, right_motor, wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)

# Gyro on before the reset, so the reset also zeros the gyro.
drive_base.use_gyro(True)

# Fixed speeds so every run behaves the same.
drive_base.settings(straight_speed=300, straight_acceleration=600, turn_rate=200, turn_acceleration=400)

# Let the robot settle so the gyro zeros cleanly. Give up after 2 seconds.
settle_timer = StopWatch()
while not hub.imu.stationary() and settle_timer.time() < 2000:
    wait(10)

# Resets distance, heading, and gyro in one call.
drive_base.straight(-10)
drive_base.reset()

# Write your code. 
#drive_base.straight(100)
#drive_base.straight(-100)
drive_base.stop()

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait


# -------------------------------------------------------------
# 1. Hardware setup
# -------------------------------------------------------------

# Create the hub object.
# This also gives access to the built in gyro, which Pybricks calls the IMU.
hub = PrimeHub()

# Drive motors.
# Direction is chosen so that a positive value moves the robot forward.
# CHECK THIS: your earlier build had left on Port.E and right on Port.A.
# If the robot turns the wrong way, the two ports are swapped.
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E, Direction.CLOCKWISE)

# Attachment motors.
# Uncomment these only if the motors are actually plugged in.
# Creating a Motor on an empty port will raise an error and stop the program.
# arm_motor = Motor(Port.B)
# lift_motor = Motor(Port.C)


# -------------------------------------------------------------
# 2. Robot measurements
# -------------------------------------------------------------

# Wheel diameter in mm.
# 56 mm is the small SPIKE Prime wheel. 62.4 mm is the large one.
# If the robot drives too far, increase this value slightly.
# If it drives too short, decrease it slightly.
WHEEL_DIAMETER = 56

# Axle track in mm. This is the distance between the centers of the two wheels.
# If turns overshoot, reduce this value. If turns undershoot, increase it.
AXLE_TRACK = 164

drive_base = DriveBase(
    left_motor,
    right_motor,
    wheel_diameter=WHEEL_DIAMETER,
    axle_track=AXLE_TRACK,
)

# Use the gyro so the robot holds a straight line and turns accurately.
drive_base.use_gyro(True)

# -------------------------------------------------------------
# 3. Start of run reset
# -------------------------------------------------------------
drive_base.straight(-10)
drive_base.reset()

# Drive forward 400 mm. The gyro keeps the line straight.
drive_base.straight(415)

# Drive backward 100 mm. A negative value means reverse.

drive_base.straight(-375)
drive_base.stop()
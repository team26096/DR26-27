from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# Initialize the hub
hub = PrimeHub()

# Drive motors setup
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E, Direction.CLOCKWISE)

# Attachment motors setup
# Updated with Port C as left attachment and Port B as right attachment
attachment_left = Motor(Port.B, gears=[[20, 12], [12, 36], [12, 20]])
attachment_right = Motor(Port.C, gears=[[20, 12], [12, 36], [12, 20]])

# DriveBase setup
WHEEL_DIAMETER = 56
AXLE_TRACK = 164

drive_base = DriveBase(
    left_motor,
    right_motor,
    wheel_diameter=WHEEL_DIAMETER,
    axle_track=AXLE_TRACK,
)
drive_base.use_gyro(True)

# -------------------------------------------------------------
# Reset & Calibration
# -------------------------------------------------------------
drive_base.stop()

while not hub.imu.ready():
    wait(10)

for _ in range(300):
    if hub.imu.stationary():
        break
    wait(10)

left_motor.reset_angle(0)
right_motor.reset_angle(0)
hub.imu.reset_heading(0)
drive_base.reset()
wait(100)

# -------------------------------------------------------------
# Mission Actions
# -------------------------------------------------------------

# Lift left attachment arm (Port B) by 90 degrees
attachment_left.run_angle(speed=200, rotation_angle=-90, then=Stop.HOLD)

# Stop drive base
drive_base.stop()
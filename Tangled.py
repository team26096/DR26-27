from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# 1. Initialize the hub
hub = PrimeHub()

# 2. Setup Drive Motors and DriveBase
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E, Direction.CLOCKWISE)

drive_base = DriveBase(
    left_motor,
    right_motor,
    wheel_diameter=56,
    axle_track=164,
)
drive_base.use_gyro(True)

# 3. Setup Attachment Motors
right_attachment = Motor(Port.B, gears=[[20, 12], [12, 36], [12, 20]])
left_attachment = Motor(Port.C, gears=[[20, 12], [12, 36], [12, 20]])

# 4. Calibration and Reset
def reset_robot():
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

reset_robot()

# Raise Port B arm by 20 degrees at 200 deg/s and hold position
right_attachment.run_angle(speed=600, rotation_angle=100, then=Stop.HOLD)
# Ensure drive base remains stopped
drive_base.stop()
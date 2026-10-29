
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ForceSensor, Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

watch = StopWatch()

# Initialize the hub
hub = PrimeHub()

# Drive motors setup
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E, Direction.CLOCKWISE)

# Attachment motors setup
# 1:1 bevel gear ratio means 1 degree of motor rotation = 1 degree of arm movement
attachment_right = Motor(Port.C, gears=[[12,20],[12,20]])
attachment_left = Motor(Port.B, gears=[[12,20],[12,36]])

# DriveBase setup
WHEEL_DIAMETER = 62.4
AXLE_TRACK = 151

drive_base = DriveBase(left_motor, right_motor, wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)
drive_base.use_gyro(True)

drive_base.settings(straight_speed=500, straight_acceleration=(800,400),
                    turn_rate=200, turn_acceleration=200)

# left_motor.reset_angle(0)
hub.imu.reset_heading(0)



# Takes up slack in the gears.
drive_base.straight(-10)

drive_base.reset()
drive_base.straight(570)
drive_base.arc(10,90)
drive_base.straight(190) 
drive_base.arc(-82, angle=90)
drive_base.straight(150)   
attachment_right.run_angle(speed=600, rotation_angle=60, then=Stop.HOLD)
drive_base.straight(-140) 
attachment_right.run_angle(speed=600, rotation_angle=-60, then=Stop.HOLD)

attachment_right.run_angle(speed=600, rotation_angle=60, then=Stop.HOLD)
drive_base.arc(82, angle=-90)

drive_base.straight(-170, wait=False)
timer = StopWatch()
while not drive_base.done():
    if timer.time() > 1500:
        drive_base.stop()
        break
    wait(10)
 
drive_base.straight(150, then=Stop.NONE) 
drive_base.arc(-450,distance=750) 
drive_base.stop()   

# TIMER STOP. pause() freezes the value so it cannot creep up after this line.
watch.pause()

# time() returns milliseconds, so divide by 1000 to get seconds.
elapsed = round(watch.time() / 1000, 1)
print("Total run time:", elapsed, "seconds")

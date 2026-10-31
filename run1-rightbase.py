# Run 1: right base.
# Upload without starting:
# pybricksdev run ble .\run1-rightbase.py --no-start --name pixiebricks

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, wait

timer = StopWatch()
hub = PrimeHub()

# Drive motors
left_drive = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_drive = Motor(Port.E, Direction.CLOCKWISE)
drivebase = DriveBase(
    left_drive,
    right_drive,
    wheel_diameter=62.4,
    axle_track=151,
)


drivebase.use_gyro(True)

# PixieBricks keeps its original hub PID defaults; only MickeyBricks is tuned.
if hub.system.info()["name"].lower() == "mickeybricks":
    heading_pid = drivebase.heading_control.pid()
    drivebase.heading_control.pid(23000, *heading_pid[1:])

# Attachment motors
left_attach = Motor(
    Port.B,
    gears=[
        [12, 20],
        [20, 20],
    ],
)

right_attach = Motor(
    Port.C,
    gears=[
        [12, 20],
        [1, 24],
    ],
)

# Mission settings: 300 mm/s, with 400 mm/s² acceleration and deceleration.
drivebase.settings(300, (400, 400), 125, 500)
print("Robot settings:", drivebase.settings())
print("Heading PID:", drivebase.heading_control.pid())
print("Drive limits:", drivebase.distance_control.limits())
print("Left attachment limits:", left_attach.control.limits())

# Square backward against the wall for 250 ms, matching Run3's squaring duration.
# Run each wheel independently so heading control does not fight the wall.
drivebase.stop()
try:
    left_drive.run_time(-60, 250, then=Stop.BRAKE, wait=False)
    right_drive.run_time(-60, 250, then=Stop.BRAKE, wait=False)
    wait(250)
finally:
    left_drive.brake()
    right_drive.brake()
wait(100)
drivebase.reset()

# Humongous Fungus: home the arm against its upper stop.
left_attach.run_until_stalled(
    500,
    then=Stop.HOLD,
    duty_limit=25,
)

left_attach.reset_angle(0)
# Lower the arm, approach, and flick the fungus upward.
left_attach.run_angle(speed=-360, rotation_angle=120, then=Stop.HOLD, wait=True)
drivebase.straight(770)
print("Distance:", drivebase.distance())
print("Heading (deg):", hub.imu.heading())
print("Battery (mV):", hub.battery.voltage())

left_attach.run_angle(speed=-600, rotation_angle=-90, then=Stop.HOLD, wait=True)

# Keystone Species: withdraw, turn, approach, and release.
drivebase.straight(-40)
drivebase.turn(45)
drivebase.straight(160)

right_attach.run_angle(speed=360, rotation_angle=80, then=Stop.HOLD, wait=True)
right_attach.run_angle(speed=360, rotation_angle=-30, then=Stop.HOLD, wait=False)

# Lower slowly throughout the reverse and turn toward Forest Elder.
arm_timer = StopWatch()
left_attach.run_angle(speed=-50, rotation_angle=120, then=Stop.HOLD, wait=False)
drivebase.straight(-120)

drivebase.turn(45)
# Allow up to four seconds total for lowering, including the reverse and turn.
while not left_attach.done():
    if arm_timer.time() >= 4000:
        drivebase.brake()
        left_attach.hold()
        raise RuntimeError("Left arm lowering timed out before Forest Elder")
    wait(10)

# Forest Elder: approach and lift the support.
drivebase.straight(60)
left_attach.run_angle(speed=-400, rotation_angle=-45, then=Stop.HOLD, wait=True)

drivebase.arc(75.5, angle=-90)
# Fast return to base.
drivebase.settings(500, (800, 400), 125, 500)
drivebase.straight(-650)

elapsed_seconds = timer.time() / 1000
print("Elapsed time: {:.2f} seconds".format(elapsed_seconds))

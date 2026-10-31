# Run 3: right base, leftmost bold black line fully visible.

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, wait

timer = StopWatch()
hub = PrimeHub()

left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E, Direction.CLOCKWISE)

drivebase = DriveBase(
    left_motor,
    right_motor,
    wheel_diameter=62.4,
    axle_track=151,
)

drivebase.use_gyro(True)

# PixieBricks keeps its original hub PID defaults; only MickeyBricks is tuned.
if hub.system.info()["name"].lower() == "mickeybricks":
    heading_pid = drivebase.heading_control.pid()
    drivebase.heading_control.pid(23000, *heading_pid[1:])

# Mission approach settings and diagnostics.
drivebase.settings(300, (400, 400), 125, (500, 250))
current_settings = drivebase.settings()
print("Robot Settings:", current_settings)
print("Heading PID:", drivebase.heading_control.pid())
print("Robot max", drivebase.distance_control.limits())
print("Turn max", drivebase.heading_control.limits())
print("Stall tolerances", drivebase.heading_control.stall_tolerances())

# Square forward against the wall before resetting distance and heading.
# Run each wheel independently so heading control does not fight the wall.
drivebase.stop()
try:
    left_motor.run_time(60, 500, then=Stop.BRAKE, wait=False)
    right_motor.run_time(60, 500, then=Stop.BRAKE, wait=False)
    wait(250)
finally:
    left_motor.brake()
    right_motor.brake()
wait(100)

drivebase.reset()
drivebase.straight(-525, then=Stop.NONE)
drivebase.arc(210, angle=-90, then=Stop.NONE)
drivebase.straight(-150)
drivebase.turn(135)

# Push slowly, then withdraw to free the attachment.
drivebase.drive(-50, 0)
wait(2750)
drivebase.stop()

# Wheel pivot for the window drive-by.
drivebase.straight(30)
drivebase.arc(-75.5, -90)

# Faster settings for the trip home.
drivebase.settings(500, (800, 400), 250, (700, 400))
# Curved return to right home.
drivebase.straight(-300)
drivebase.arc(-75.5, angle=drivebase.angle() - 180)
drivebase.straight(-350)

elapsed_seconds = timer.time() / 1000
print("Elapsed time: {:.2f} seconds".format(elapsed_seconds))

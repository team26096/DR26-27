# Run 3: right base, leftmost bold black line fully visible.

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, wait


def run(drivebase):
    timer = StopWatch()

    # Loaded here, not at the top, because helpers.py needs config.py to finish first.
    from helpers import hub, left_motor, right_motor

    # PixieBricks keeps its original hub PID defaults; only MickeyBricks is tuned.
    if hub.system.info()["name"].lower() == "mickeybricks":
        heading_pid = drivebase.heading_control.pid()
        drivebase.heading_control.pid(23000, *heading_pid[1:])

    # Loaded here, not at the top, because config.py loads this file first.
    from config import START, FINISH

    # Mission approach settings (start speeds from config.py) and diagnostics.
    # CHANGE (Nov 9): was drivebase.settings(300, (400, 400), 125, (500, 250)).
    drivebase.settings(**START)
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

    # Faster settings for the trip home (finish speeds from config.py).
    # CHANGE (Nov 9): was drivebase.settings(500, (800, 400), 250, (700, 400)).
    drivebase.settings(**FINISH)
    # Curved return to right home.
    drivebase.straight(-300)
    drivebase.arc(-75.5, angle=drivebase.angle() - 180)
    drivebase.straight(-370)

    elapsed_seconds = timer.time() / 1000
    print("Elapsed time: {:.2f} seconds".format(elapsed_seconds))


# Only happens when this file is uploaded by itself. The menu in main.py skips
# this and calls run() instead.
if __name__ == "__main__":
    from helpers import run_alone
    run_alone(run)

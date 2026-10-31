from pybricks.parameters import Stop
from pybricks.tools import wait


def run(drive_base, attachment_left, attachment_right):
    # Run 3: right base, leftmost bold black line fully visible.
    # Same moves as run3-rightbase.py.

    # Loaded here, not at the top, because helpers.py needs config.py to finish first.
    from helpers import hub, left_motor, right_motor

    # PixieBricks keeps its original hub PID defaults; only MickeyBricks is tuned.
    if hub.system.info()["name"].lower() == "mickeybricks":
        heading_pid = drive_base.heading_control.pid()
        drive_base.heading_control.pid(23000, *heading_pid[1:])

    # Mission approach settings and diagnostics.
    drive_base.settings(300, (400, 400), 125, (500, 250))
    current_settings = drive_base.settings()
    print("Robot Settings:", current_settings)
    print("Heading PID:", drive_base.heading_control.pid())
    print("Robot max", drive_base.distance_control.limits())
    print("Turn max", drive_base.heading_control.limits())
    print("Stall tolerances", drive_base.heading_control.stall_tolerances())

    # main.py backs up 5 mm before every run, which is away from the wall here.
    # Go forward 5 mm so squaring starts from the same spot as run3-rightbase.py.
    drive_base.straight(5)

    # Square forward against the wall before resetting distance and heading.
    # Run each wheel independently so heading control does not fight the wall.
    drive_base.stop()
    try:
        left_motor.run_time(60, 500, then=Stop.BRAKE, wait=False)
        right_motor.run_time(60, 500, then=Stop.BRAKE, wait=False)
        wait(250)
    finally:
        left_motor.brake()
        right_motor.brake()
    wait(100)

    drive_base.reset()
    drive_base.straight(-525, then=Stop.NONE)
    drive_base.arc(210, angle=-90, then=Stop.NONE)
    drive_base.straight(-150)
    drive_base.turn(135)

    # Push slowly, then withdraw to free the attachment.
    drive_base.drive(-50, 0)
    wait(2750)
    drive_base.stop()

    # Wheel pivot for the window drive-by.
    drive_base.straight(30)
    drive_base.arc(-75.5, -90)

    # Faster settings for the trip home.
    drive_base.settings(500, (800, 400), 250, (700, 400))
    # Curved return to right home.
    drive_base.straight(-300)
    drive_base.arc(-75.5, angle=drive_base.angle() - 180)
    drive_base.straight(-350)

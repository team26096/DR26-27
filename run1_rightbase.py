from pybricks.parameters import Stop
from pybricks.tools import StopWatch, wait


def run(drive_base, attachment_left, attachment_right):
    # Run 1: right base. Same moves as run1-rightbase.py.

    # Loaded here, not at the top, because helpers.py needs config.py to finish first.
    from helpers import hub, left_motor, right_motor

    # PixieBricks keeps its original hub PID defaults; only MickeyBricks is tuned.
    if hub.system.info()["name"].lower() == "mickeybricks":
        heading_pid = drive_base.heading_control.pid()
        drive_base.heading_control.pid(23000, *heading_pid[1:])

    # Mission settings: 300 mm/s, with 400 mm/s² acceleration and deceleration.
    drive_base.settings(300, (400, 400), 125, 500)
    print("Robot settings:", drive_base.settings())
    print("Heading PID:", drive_base.heading_control.pid())
    print("Drive limits:", drive_base.distance_control.limits())
    print("Left attachment limits:", attachment_left.control.limits())

    # Square backward against the wall for 250 ms, matching Run3's squaring duration.
    # Run each wheel independently so heading control does not fight the wall.
    drive_base.stop()
    try:
        left_motor.run_time(-60, 250, then=Stop.BRAKE, wait=False)
        right_motor.run_time(-60, 250, then=Stop.BRAKE, wait=False)
        wait(250)
    finally:
        left_motor.brake()
        right_motor.brake()
    wait(100)
    drive_base.reset()

    # Humongous Fungus: home the arm against its upper stop.
    attachment_left.run_until_stalled(
        500,
        then=Stop.HOLD,
        duty_limit=25,
    )

    attachment_left.reset_angle(0)
    # Lower the arm, approach, and flick the fungus upward.
    attachment_left.run_angle(speed=-360, rotation_angle=120, then=Stop.HOLD, wait=True)
    drive_base.straight(770)
    print("Distance:", drive_base.distance())
    print("Heading (deg):", hub.imu.heading())
    print("Battery (mV):", hub.battery.voltage())

    attachment_left.run_angle(speed=-600, rotation_angle=-90, then=Stop.HOLD, wait=True)

    # Keystone Species: withdraw, turn, approach, and release.
    drive_base.straight(-40)
    drive_base.turn(45)
    drive_base.straight(160)

    # config.py uses different gears for this arm than run1-rightbase.py did, so
    # these numbers are 24 times bigger and turn the motor the same amount.
    attachment_right.run_angle(speed=8640, rotation_angle=1920, then=Stop.HOLD, wait=True)
    attachment_right.run_angle(speed=8640, rotation_angle=-720, then=Stop.HOLD, wait=False)

    # Lower slowly throughout the reverse and turn toward Forest Elder.
    arm_timer = StopWatch()
    attachment_left.run_angle(speed=-50, rotation_angle=120, then=Stop.HOLD, wait=False)
    drive_base.straight(-120)

    drive_base.turn(45)
    # Allow up to four seconds total for lowering, including the reverse and turn.
    while not attachment_left.done():
        if arm_timer.time() >= 4000:
            drive_base.brake()
            attachment_left.hold()
            raise RuntimeError("Left arm lowering timed out before Forest Elder")
        wait(10)

    # Forest Elder: approach and lift the support.
    drive_base.straight(60)
    attachment_left.run_angle(speed=-400, rotation_angle=-45, then=Stop.HOLD, wait=True)

    drive_base.arc(75.5, angle=-90)
    # Fast return to base.
    drive_base.settings(500, (800, 400), 125, 500)
    drive_base.straight(-650)

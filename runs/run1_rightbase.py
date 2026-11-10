# Run 1: right base.
# Upload without starting (set RUN = "7" in test_run.py first):
# pybricksdev run ble .\test_run.py --no-start --name pixiebricks

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, wait


def run(drivebase):
    left_attach = None
    right_attach = None
    try:
        timer = StopWatch()

        # Loaded here, not at the top, because lib/helpers.py needs lib/config.py to finish first.
        from lib.helpers import hub, left_motor as left_drive, right_motor as right_drive

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
                [1, 8],
            ],
        )

        # Loaded here, not at the top, because lib/config.py loads this file first.
        from lib.config import START, FINISH

        # Mission settings: start speeds from lib/config.py.
        # CHANGE (Nov 9): was drivebase.settings(300, (400, 400), 125, 500), which
        # is 300 mm/s, with 400 mm/s² acceleration and deceleration.
        drivebase.settings(**START)
        print("Robot settings:", drivebase.settings())
        print("Heading PID:", drivebase.heading_control.pid())
        print("Drive limits:", drivebase.distance_control.limits())
        print("Left attachment limits:", left_attach.control.limits())
        # CHANGE (Nov 5): also print the right attachment limits, not just the left.
        print("Right attachment limits:", right_attach.control.limits())

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

        # CHANGE (Nov 5): new way back to base.
        # Before: arc(75.5, angle=-90), then drive backward 650 mm (straight(-650)).
        # Now: back up 80 mm, arc the other way (angle=90), then drive forward
        # 650 mm. then=Stop.NONE lets the robot roll straight into the next move
        # without stopping after the arc. The left arm also moves 30 degrees while
        # the robot drives back, because wait=False lets both happen at once.
        # drivebase.straight(-80)
        drivebase.arc(75.5, angle=-90) #removed stop=Stop.NONE to see if it helps with the arc
        # Fast return to base (finish speeds from lib/config.py).
        # CHANGE (Nov 9): was drivebase.settings(500, (800, 400), 125, 500).
        drivebase.settings(**FINISH)
        left_attach.run_angle(speed=-400, rotation_angle=-30, then=Stop.HOLD, wait=False)
        drivebase.straight(-650)

        elapsed_seconds = timer.time() / 1000
        print("Elapsed time: {:.2f} seconds".format(elapsed_seconds))

        # Save the final angles before releasing the attachment ports.
        return (left_attach.angle(), right_attach.angle())
    finally:
        if left_attach is not None:
            left_attach.close()
        if right_attach is not None:
            right_attach.close()


# Only happens when this file is started by itself. The menu in main.py skips
# this and calls run() instead.
# CHANGE (Nov 10): this file moved to the runs folder. Started from here, it
# can't load lib/helpers.py, because the hub only gets the files it can find
# next to the file you start. To test this run by itself, start test_run.py in
# the main folder. Before, this part started the run with run_alone().
if __name__ == "__main__":
    print("To test this run by itself, start test_run.py in the main folder.")

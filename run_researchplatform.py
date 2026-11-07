from pybricks.parameters import Port, Stop
from pybricks.pupdevices import Motor
from pybricks.tools import wait, StopWatch


def run(drive_base):
    attachment_left = None
    attachment_right = None
    try:
        # Research Platform. Same code as ResearchPlatform.py.

        # Loaded here, not at the top, because helpers.py needs config.py to finish first.
        from helpers import hub

        watch = StopWatch()

        # Attachment motors setup
        attachment_right = Motor(Port.C, gears=[[12,20],[12,20]])
        attachment_left = Motor(Port.B, gears=[[12,20],[12,36]])

        drive_base.settings(straight_speed=500, straight_acceleration=(800,400),
                            turn_rate=200, turn_acceleration=200)

        # left_motor.reset_angle(0)
        hub.imu.reset_heading(0)

        # Takes up slack in the gears.
        drive_base.straight(-10)

        drive_base.reset()
        drive_base.straight(570)
        # CHANGE (Nov 5): new step. The right attachment turns 120 degrees here,
        # after driving out and before the arc. Before this, the first right
        # attachment move was the 60 degree one after straight(150) below.
        attachment_right.run_angle(speed=600, rotation_angle=-120, then=Stop.HOLD)
        drive_base.arc(10,90)
        drive_base.straight(190)
        drive_base.arc(-82, angle=90)
        drive_base.straight(150)
        attachment_right.run_angle(speed=600, rotation_angle=60, then=Stop.HOLD)
        drive_base.straight(-140)
        attachment_right.run_angle(speed=600, rotation_angle=-60, then=Stop.HOLD)

        attachment_right.run_angle(speed=600, rotation_angle=60, then=Stop.HOLD)
        drive_base.arc(82, angle=-90)

        # Back up 200 mm, but stop after 1 second even if it has not finished.
        # CHANGE (Nov 5): was straight(-170) with a 1.5 second limit. Now -200
        # with a 1 second limit, and it prints TIMED OUT when the limit is hit.
        # Note: at these speeds the full 200 mm takes about 1.2 seconds, so the
        # 1 second limit usually stops it first, at about 190 mm. That means
        # TIMED OUT prints even when nothing went wrong. The old 170 mm took
        # about 1.1 seconds and finished before its 1.5 second limit.
        # start is saved but not used anywhere yet.
        start = drive_base.distance()
        drive_base.straight(-200, wait=False)
        timer = StopWatch()
        while not drive_base.done():
            if timer.time() > 1000:
                drive_base.stop()
                print("TIMED OUT")
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

        # Save the final angles before releasing the attachment ports.
        return (attachment_left.angle(), attachment_right.angle())
    finally:
        if attachment_left is not None:
            attachment_left.close()
        if attachment_right is not None:
            attachment_right.close()


# Only happens when this file is uploaded by itself. The menu in main.py skips
# this and calls run() instead.
if __name__ == "__main__":
    from helpers import run_alone
    run_alone(run)

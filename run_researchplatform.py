from pybricks.parameters import Stop
from pybricks.tools import StopWatch, wait


def run(drive_base, attachment_left, attachment_right):
    # Research Platform. Same moves as ResearchPlatform.py.

    # Loaded here, not at the top, because helpers.py needs config.py to finish first.
    # main.py passes in the distance tracker, which has no done(), so the timed
    # back up below asks the real drive base instead.
    from helpers import drive_base as real_drive_base

    drive_base.settings(straight_speed=500, straight_acceleration=(800, 400),
                        turn_rate=200, turn_acceleration=200)

    # Takes up slack in the gears. main.py already backed up 5 mm, so this is
    # the other 5 mm of the 10 mm in ResearchPlatform.py.
    drive_base.straight(-5)

    drive_base.reset()
    drive_base.straight(570)
    drive_base.arc(10, 90)
    drive_base.straight(190)
    drive_base.arc(-82, angle=90)
    drive_base.straight(150)

    # config.py uses different gears for this arm than ResearchPlatform.py did,
    # so 100 and 1000 here turn the motor the same amount as 60 and 600 did there.
    attachment_right.run_angle(speed=1000, rotation_angle=100, then=Stop.HOLD)
    drive_base.straight(-140)
    attachment_right.run_angle(speed=1000, rotation_angle=-100, then=Stop.HOLD)

    attachment_right.run_angle(speed=1000, rotation_angle=100, then=Stop.HOLD)
    drive_base.arc(82, angle=-90)

    # Back up for at most 1.5 seconds, in case something stops the robot.
    drive_base.straight(-170, wait=False)
    timer = StopWatch()
    while not real_drive_base.done():
        if timer.time() > 1500:
            drive_base.stop()
            break
        wait(10)

    drive_base.straight(150, then=Stop.NONE)
    drive_base.arc(-450, distance=750)

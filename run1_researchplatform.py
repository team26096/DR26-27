from pybricks.parameters import Stop


def run(drive_base, attachment_left, attachment_right):
    # Research Platform. Uses the right arm.

    # Faster than the speed in config.py. main.py sets it back before the next run.
    drive_base.settings(straight_speed=600)

    drive_base.straight(570)
    drive_base.arc(10, angle=90)
    drive_base.straight(190)
    drive_base.arc(-82, angle=90)
    drive_base.straight(150)

    # config.py uses different gears for this arm than ResearchPlatform.py did,
    # so 75 and 1000 here turn the motor the same amount as 45 and 600 did there.
    attachment_right.run_angle(speed=1000, rotation_angle=75, then=Stop.HOLD)
    drive_base.straight(-150)
    attachment_right.run_angle(speed=1000, rotation_angle=-75, then=Stop.HOLD)

from pybricks.parameters import Stop


def run(drive_base, attachment_left, attachment_right):
    # Forest Elder seed collection. Same moves as forest_elder_seed_collection.py.

    # Loaded here, not at the top, because helpers.py needs config.py to finish first.
    from helpers import default_settings

    # forest_elder_seed_collection.py only set the straight speeds, so its turns
    # used Pybricks' own speeds and not the ones in config.py.
    drive_base.settings(straight_speed=500, straight_acceleration=400,
                        turn_rate=default_settings[2],
                        turn_acceleration=default_settings[3])
    print("Robot Settings:", drive_base.settings())

    # Takes up slack in the gears. main.py already backed up 5 mm, so this is
    # the other 5 mm of the 10 mm in forest_elder_seed_collection.py.
    drive_base.straight(-5)

    attachment_right.run_until_stalled(200, then=Stop.HOLD, duty_limit=25)

    # 1. Drive forward
    drive_base.straight(410)
    drive_base.stop()
    drive_base.reset()

    # 2. Rotate the entire robot
    drive_base.turn(37)

    drive_base.straight(112)

    # config.py uses different gears for this arm than
    # forest_elder_seed_collection.py did, so 105 and 270 here turn the motor the
    # same amount as 35 and 90 did there.
    attachment_left.run_angle(speed=270, rotation_angle=105, then=Stop.HOLD, wait=True)

    attachment_right.run_angle(speed=200, rotation_angle=-50, then=Stop.HOLD, wait=True)

    drive_base.straight(-160)

    attachment_right.run_angle(speed=200, rotation_angle=30, then=Stop.HOLD, wait=True)

    drive_base.straight(-120)
    drive_base.turn(-12)
    drive_base.turn(-80)
    drive_base.straight(-350)

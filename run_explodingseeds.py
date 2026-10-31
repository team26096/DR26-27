from pybricks.parameters import Stop
from pybricks.tools import StopWatch


def run(drive_base, attachment_left, attachment_right):
    # Exploding Seeds, Biocentric Architecture, and Window to the Past.
    # Same moves as ExplodingSeeds.py.

    # Loaded here, not at the top, because helpers.py needs config.py to finish first.
    from helpers import default_settings

    watch = StopWatch()

    # ExplodingSeeds.py only set the straight speed, so everything else used
    # Pybricks' own speeds and not the ones in config.py.
    drive_base.settings(straight_speed=600,
                        straight_acceleration=default_settings[1],
                        turn_rate=default_settings[2],
                        turn_acceleration=default_settings[3])

    # main.py backs up 5 mm before every run. Go forward 5 mm so this run starts
    # from the same spot as ExplodingSeeds.py.
    drive_base.straight(5)

    # config.py uses different gears for both arms than ExplodingSeeds.py did, so
    # the arm numbers here turn the motors the same amount as the ones there.
    # Left arm: speeds and angles are 3 times bigger.
    # Right arm: speeds and angles are 5/3 bigger, rounded to whole numbers.

    # Drive forward from base to start aligning with Exploding Seeds.
    drive_base.straight(200, wait=False)

    # Lift the left arm until it stalls, to set up for Biocentric Architecture.
    attachment_left.run_until_stalled(-510, then=Stop.HOLD, duty_limit=35)

    # Turn to keep aligning with Exploding Seeds.
    drive_base.turn(50)

    # Go forward to make contact with the seed.
    drive_base.settings(straight_speed=400)
    drive_base.straight(320)

    # Lift the right arm to align for seed removal.
    attachment_right.run_angle(speed=333, rotation_angle=33)

    drive_base.settings(straight_speed=100)

    # Lift the arm slightly and back up, twice, to get the seed out.
    attachment_right.run_angle(speed=83, rotation_angle=8)
    drive_base.straight(-18)
    attachment_right.run_angle(speed=42, rotation_angle=8)
    drive_base.straight(-15)

    attachment_right.run_angle(speed=17, rotation_angle=37)

    drive_base.settings(straight_speed=300)

    # Back up to get clear of Exploding Seeds.
    drive_base.straight(-200)

    print("Timestamp after picking up seeds:", watch.time() / 1000)

    # Turn to line up with Biocentric Architecture.
    drive_base.turn(33)

    drive_base.settings(straight_speed=300)

    # Lower the left arm while driving to Biocentric Architecture.
    attachment_left.run_angle(speed=600, rotation_angle=480, wait=False)
    drive_base.straight(610)

    drive_base.settings(straight_speed=100)

    # Turn left slightly to align with Biocentric Architecture.
    drive_base.turn(-20)

    # Arm down to complete the compost hatch.
    attachment_left.run_angle(speed=300, rotation_angle=60)

    # Arm up to complete the nesting canopy.
    attachment_left.run_angle(speed=75, rotation_angle=-135)

    # Arm down again to make sure the compost hatch is complete.
    attachment_left.run_angle(speed=300, rotation_angle=135)

    drive_base.settings(straight_speed=250)

    # Turn right to move away from Biocentric Architecture.
    drive_base.turn(20)

    # Lower the right arm to align for the Window to the Past seed.
    attachment_right.run_angle(speed=167, rotation_angle=-50, wait=False)

    # Move forward to start aligning with the seed.
    drive_base.straight(130)

    # Turn left to line up with the seed.
    drive_base.turn(-20)

    # Move forward so the right arm is under the seed, while lifting the left arm.
    drive_base.straight(120, wait=False)
    attachment_left.run_angle(speed=1500, rotation_angle=-360)

    # Lift the right arm to pick up the seed.
    attachment_right.run_angle(speed=167, rotation_angle=100)

    drive_base.arc(50, -130)

    drive_base.settings(straight_speed=500)

    drive_base.straight(-650)

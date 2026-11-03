from pybricks.parameters import Port, Stop
from pybricks.pupdevices import Motor
from pybricks.tools import StopWatch


def run(drive_base):
    attachment_left = None
    attachment_right = None
    try:
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

        # Attachment gears from ExplodingSeeds.py, for this run only.
        attachment_right = Motor(Port.C, gears=[[12,20],[12,20]])
        attachment_left = Motor(Port.B, gears=[[12,20],[12,36]])

        # Drive forward from base to start aligning with Exploding Seeds.
        drive_base.straight(200, wait=False)

        # Lift the left arm until it stalls, to set up for Biocentric Architecture.
        attachment_left.run_until_stalled(-170, then=Stop.HOLD, duty_limit=35)

        # Turn to keep aligning with Exploding Seeds.
        drive_base.turn(50)

        # Go forward to make contact with the seed.
        drive_base.settings(straight_speed=400)
        drive_base.straight(320)

        # Lift the right arm to align for seed removal.
        attachment_right.run_angle(speed=200, rotation_angle=20)

        drive_base.settings(straight_speed=100)

        # Lift the arm slightly and back up, twice, to get the seed out.
        attachment_right.run_angle(speed=50, rotation_angle=5)
        drive_base.straight(-18)
        attachment_right.run_angle(speed=25, rotation_angle=5)
        drive_base.straight(-15)

        attachment_right.run_angle(speed=10, rotation_angle=22)

        drive_base.settings(straight_speed=300)

        # Back up to get clear of Exploding Seeds.
        drive_base.straight(-200)

        print("Timestamp after picking up seeds:", watch.time() / 1000)

        # Turn to line up with Biocentric Architecture.
        drive_base.turn(33)

        drive_base.settings(straight_speed=300)

        # Lower the left arm while driving to Biocentric Architecture.
        attachment_left.run_angle(speed=200, rotation_angle=160, wait=False)
        drive_base.straight(610)

        drive_base.settings(straight_speed=100)

        # Turn left slightly to align with Biocentric Architecture.
        drive_base.turn(-20)

        # Arm down to complete the compost hatch.
        attachment_left.run_angle(speed=100, rotation_angle=20)

        # Arm up to complete the nesting canopy.
        attachment_left.run_angle(speed=25, rotation_angle=-45)

        # Arm down again to make sure the compost hatch is complete.
        attachment_left.run_angle(speed=100, rotation_angle=45)

        drive_base.settings(straight_speed=250)

        # Turn right to move away from Biocentric Architecture.
        drive_base.turn(20)

        # Lower the right arm to align for the Window to the Past seed.
        attachment_right.run_angle(speed=100, rotation_angle=-30, wait=False)

        # Move forward to start aligning with the seed.
        drive_base.straight(130)

        # Turn left to line up with the seed.
        drive_base.turn(-20)

        # Move forward so the right arm is under the seed, while lifting the left arm.
        drive_base.straight(120, wait=False)
        attachment_left.run_angle(speed=500, rotation_angle=-120)

        # Lift the right arm to pick up the seed.
        attachment_right.run_angle(speed=100, rotation_angle=60)

        drive_base.arc(50, -130)

        drive_base.settings(straight_speed=500)

        drive_base.straight(-650)

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

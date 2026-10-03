def run(drive_base, attachment_left, attachment_right):
    # Robot run 1: Flip the Rock
    # This run does not use the attachments.
    print("Robot run 1: Flip the Rock")

    # The old file used a 56 mm wheel size, but main.py uses 62.4 mm.
    # The numbers below are the old numbers times 1.114,
    # so the robot moves the same real distance as before.
    # Old numbers: 10, -415, 375

    # Take up slack in the gears, then zero the distance.
    drive_base.straight(11)
    drive_base.reset()

    # The robot starts facing backward.
    # A negative number drives it backward, toward the rock.
    drive_base.straight(-462)

    # A positive number drives it forward, back toward base.
    drive_base.straight(418)

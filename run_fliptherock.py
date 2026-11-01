def run(drive_base, attachment_left, attachment_right):
    # Flip the Rock. No attachments. Same moves as FlipTheRock.py.

    # Loaded here, not at the top, because helpers.py needs config.py to finish first.
    from helpers import default_settings

    # FlipTheRock.py never set any speeds, so it used Pybricks' own speeds and not
    # the ones in config.py.
    drive_base.settings(straight_speed=default_settings[0],
                        straight_acceleration=default_settings[1],
                        turn_rate=default_settings[2],
                        turn_acceleration=default_settings[3])


    drive_base.straight(-10)
    drive_base.reset()

    # The robot starts facing the rock, so positive drives toward it.
    drive_base.straight(430)

    # Negative drives backward, back toward base.
    drive_base.straight(-375)
    drive_base.stop()


# Only happens when this file is uploaded by itself. The menu in main.py skips
# this and calls run() instead.
if __name__ == "__main__":
    from helpers import run_alone
    run_alone(run)

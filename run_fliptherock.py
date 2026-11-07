def run(drive_base):
    # Flip the Rock. No attachments. Same moves as FlipTheRock.py.

    # Loaded here, not at the top, because helpers.py needs config.py to finish first.
    from helpers import default_settings

    # FlipTheRock.py never set any speeds, so it used Pybricks' own speeds and not
    # the ones in config.py.
    drive_base.settings(straight_speed=300,
                        straight_acceleration=400,
                        turn_rate=200,
                        turn_acceleration=200)


    drive_base.straight(-10)
    drive_base.reset()

    # The robot starts facing the rock, so positive drives toward it.
    drive_base.straight(430)

    # Negative drives backward, back toward base.
    drive_base.straight(-325)
    drive_base.stop()

  
    #drive_base.arc(82, angle=90)
    drive_base.turn(90)
# Only happens when this file is uploaded by itself. The menu in main.py skips
# this and calls run() instead.
if __name__ == "__main__":
    from helpers import run_alone
    run_alone(run)

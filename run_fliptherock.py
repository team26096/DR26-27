from pybricks.tools import wait, StopWatch


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
    # If the rock blocks the wheels before 430 mm, straight() would wait forever.
    # So start the move without waiting, and stop pushing if the wheels stall
    # or 3 seconds pass.
    drive_base.straight(430, wait=False)
    push_timer = StopWatch()
    while not drive_base.done():
        if drive_base.stalled() or push_timer.time() > 3000:
            break
        wait(10)
    drive_base.stop()

    # Negative drives backward, back toward base.
    # straight() has no speed setting, so change the speed first.
    drive_base.settings(straight_speed=500)
    drive_base.straight(-250)
    drive_base.stop()

  
    #drive_base.arc(82, angle=90)
    drive_base.turn(90)
# Only happens when this file is uploaded by itself. The menu in main.py skips
# this and calls run() instead.
if __name__ == "__main__":
    from helpers import run_alone
    run_alone(run)

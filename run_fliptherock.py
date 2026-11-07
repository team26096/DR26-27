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
    # If the rock blocks the robot before 430 mm, straight() would wait forever.
    # So we stop when the move is done, the wheels stall, or 2.5 seconds pass.
    # A full push takes about 2.2 seconds at these speeds. If you slow the robot
    # down, raise the 2500 below, or the robot will stop before it reaches the rock.
    from pybricks.tools import wait, StopWatch
    drive_base.straight(430, wait=False)
    push_timer = StopWatch()
    while not drive_base.done():
        if drive_base.stalled() or push_timer.time() > 2500:
            break
        wait(10)
    drive_base.stop()

    # Negative drives backward, back toward base.
    # straight() has no speed setting, so change the speed first.
    drive_base.settings(straight_speed=500)
    drive_base.straight(-325)
    drive_base.stop()

  
    #drive_base.arc(82, angle=90)
    drive_base.turn(90)
# Only happens when this file is uploaded by itself. The menu in main.py skips
# this and calls run() instead.
if __name__ == "__main__":
    from helpers import run_alone
    run_alone(run)

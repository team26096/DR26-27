def run(drive_base):
    # Flip the Rock. No attachments. Same moves as FlipTheRock.py.

    # Loaded here, not at the top, because helpers.py needs config.py to finish first.
    from helpers import default_settings

    # FlipTheRock.py never set any speeds, so it used Pybricks' own speeds and not
    # the ones in config.py.
    # Loaded here, not at the top, because config.py loads this file first.
    from config import START, FINISH

    # Start speeds from config.py.
    # CHANGE (Nov 9): was straight_speed=250, straight_acceleration=200,
    # turn_rate=200, turn_acceleration=200. The push below stops after 2.5
    # seconds. If you make START slower than 250 mm/s, raise that time.
    # drive_base.settings(**START)
    drive_base.settings(straight_speed=250, straight_acceleration=200, turn_rate=200, turn_acceleration=200)

    drive_base.straight(-10)
    drive_base.reset()

    # The robot starts facing the rock, so positive drives toward it.
    # If the rock blocks the robot before 430 mm, straight() would wait forever.
    # So we stop when the move is done, the wheels stall, or 2.5 seconds pass.
    # A full push takes about 2.2 seconds at these speeds. If you slow the robot
    # down, raise the 2500 below, or the robot will stop before it reaches the rock.
    # CHANGE (Nov 5): was drive_base.straight(430) on its own. That got stuck
    # forever when the rock blocked the robot. The time limit was 3 seconds.
    # CHANGE (Nov 7): time limit lowered from 3 to 2.5 seconds, so the run ends
    # sooner when the robot is blocked.
    from pybricks.tools import wait, StopWatch
    from pybricks.parameters import Port, Direction, Stop

    drive_base.straight(470, wait=False)
    push_timer = StopWatch()
    while not drive_base.done():
        if drive_base.stalled() or push_timer.time() > 2500:
            break
        wait(10)
    drive_base.stop()

    # Negative drives backward, back toward base.
    # straight() has no speed setting, so change the speed first.
    # CHANGE (Nov 5): return speed raised from 300 to 500 mm/s, to get back to
    # base faster.
    # CHANGE (Nov 6): distance changed from -250 to -325, so the robot goes fully
    # back into base. That number was picked when the return was still 300 mm/s,
    # so check that the robot still ends inside base at 500 mm/s.
    # Finish speeds from config.py.
    # CHANGE (Nov 9): was straight_speed=500, straight_acceleration=800.
    drive_base.settings(**FINISH)
    drive_base.straight(-340, then=Stop.NONE)
    #drive_base.stop()

  
    #drive_base.arc(82, angle=90)
    # drive_base.turn(90)
# Only happens when this file is uploaded by itself. The menu in main.py skips
# this and calls run() instead.
if __name__ == "__main__":
    from helpers import run_alone
    run_alone(run)

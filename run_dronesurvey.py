from pybricks.tools import wait


def run(drive_base):
    # Drone Survey. No attachments. Same moves as DroneSurvey.py.

    # Loaded here, not at the top, because config.py loads this file first.
    from config import START, FINISH

    # Start speeds from config.py.
    # CHANGE (Nov 9): was straight_speed=300, straight_acceleration=200,
    # turn_rate=300, turn_acceleration=400.
    drive_base.settings(**START)

    drive_base.straight(650)
    drive_base.arc(-300, distance=150)
    drive_base.straight(-80)
    drive_base.drive(0, -300)

    # Keep spinning for 0.3 seconds.
    # CHANGE (Nov 5): was 1 second (wait(1000)). Now 0.3 seconds, so the run is
    # 0.7 seconds shorter and the robot turns less while it spins. The arc below
    # uses the angle the robot really turned, not a fixed number, so it still
    # matches.
    wait(300)
    drive_base.stop()

    # Finish speeds from config.py, for the way back to base.
    # CHANGE (Nov 9): was straight_speed=500, straight_acceleration=800,
    # turn_rate=500, turn_acceleration=800.
    drive_base.settings(**FINISH)

    drive_base.arc(76, angle=30)
    drive_base.straight(20)
    # CHANGE (Nov 5): the angle is saved first and printed, so you can see on the
    # computer how far the robot turned before this arc. The arc does the same
    # thing as before, which was arc(-76, angle=drive_base.angle()).
    angle = drive_base.angle()
    print("Angle before arc:", round(angle, 1), "deg")
    drive_base.arc(-76, angle=angle)
    drive_base.straight(-745)
    print("Angle after turn:", round(drive_base.angle(), 1), "deg")


# Only happens when this file is uploaded by itself. The menu in main.py skips
# this and calls run() instead.
if __name__ == "__main__":
    from helpers import run_alone
    run_alone(run)

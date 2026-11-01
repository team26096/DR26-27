from pybricks.tools import wait


def run(drive_base, attachment_left, attachment_right):
    # Drone Survey. No attachments. Same moves as DroneSurvey.py.

    drive_base.settings(straight_speed=300, straight_acceleration=200,
                        turn_rate=300, turn_acceleration=400)

    drive_base.straight(650)
    drive_base.arc(-300, distance=150)
    drive_base.straight(-80)
    drive_base.drive(0, -300)

    # Keep spinning for 1 second.
    wait(1000)
    drive_base.stop()

    drive_base.settings(straight_speed=500, straight_acceleration=800,
                        turn_rate=500, turn_acceleration=800)

    drive_base.arc(76, angle=30)
    drive_base.straight(20)
    drive_base.arc(-76, angle=drive_base.angle())
    drive_base.straight(-670)
    print("Angle after turn:", round(drive_base.angle(), 1), "deg")


# Only happens when this file is uploaded by itself. The menu in main.py skips
# this and calls run() instead.
if __name__ == "__main__":
    from helpers import run_alone
    run_alone(run)

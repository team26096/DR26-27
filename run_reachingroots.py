from pybricks.parameters import Stop


def run(drive_base, attachment_left, attachment_right):
    # Reaching Roots. Same moves as ReachingRootsNew.py.

    drive_base.settings(straight_speed=400, straight_acceleration=(800, 200),
                        turn_rate=200, turn_acceleration=200)

    # Takes up slack in the gears.
    drive_base.straight(-10)

    # straight() holds the wheels at the end. Release them before resetting.
    drive_base.stop()
    drive_base.reset()

    attachment_left.run_until_stalled(200, then=Stop.BRAKE, duty_limit=20)
    attachment_left.reset_angle(0)

    attachment_left.run_angle(speed=650, rotation_angle=-75)
    print("after move", attachment_left.angle())

    drive_base.straight(820)
    print(drive_base.distance())
    drive_base.arc(15, 90)
    attachment_left.run_angle(speed=1000, rotation_angle=-150)

    drive_base.straight(20)

    drive_base.arc(-76, angle=-45)

    drive_base.straight(-30)

    attachment_right.run_angle(speed=300, rotation_angle=-70)

    drive_base.straight(100, then=Stop.NONE)

    drive_base.turn(60, then=Stop.NONE)

    drive_base.settings(straight_speed=600, straight_acceleration=800,
                        turn_rate=200, turn_acceleration=200)

    drive_base.straight(800)

    drive_base.stop()


# Only happens when this file is uploaded by itself. The menu in main.py skips
# this and calls run() instead.
if __name__ == "__main__":
    from helpers import run_alone
    run_alone(run)

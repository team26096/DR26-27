from pybricks.parameters import Stop


def run(drive_base, attachment_left, attachment_right):
    # Reaching Roots. Same moves as ReachingRootsNew.py.

    drive_base.settings(straight_speed=300, straight_acceleration=(400, 200),
                        turn_rate=200, turn_acceleration=200)
    # Reduced speed from 400 to 300 and acceleration from 800 to 400 to reduce overshoot and improve accuracy.
    # Takes up slack in the gears.
    drive_base.straight(-10)

    # straight() holds the wheels at the end. Release them before resetting.
    drive_base.stop()
    drive_base.reset()

    attachment_left.run_until_stalled(200, then=Stop.BRAKE, duty_limit=20)
    attachment_left.reset_angle(0)
    attachment_left.run_angle(speed=650, rotation_angle=-75)
    print("after move", attachment_left.angle())

    drive_base.straight(830)
    print(drive_base.distance())
    drive_base.arc(15, 90)
    attachment_left.run_angle(speed=1000, rotation_angle=-150)
    attachment_right.run_until_stalled(-45, then=Stop.BRAKE, duty_limit=30)

    drive_base.arc(76, angle=35)
    
    attachment_right.run_angle(speed=200, rotation_angle=85)

    drive_base.straight(-100)

    attachment_right.run_angle(speed=300, rotation_angle=-100)

    drive_base.settings(straight_speed=500, straight_acceleration=(800, 800),
                        turn_rate=200, turn_acceleration=200)

    drive_base.arc(400, distance=1050)


    print("Straight PID:", drive_base.distance_control.pid())
    print("Turn PID:", drive_base.heading_control.pid())
    straight_pid = drive_base.distance_control.pid()
    heading_pid = drive_base.heading_control.pid()

    print("Straight Kp:", straight_pid[0])
    print("Straight Ki:", straight_pid[1])
    print("Straight Kd:", straight_pid[2])

    print("Heading Kp:", heading_pid[0])
    print("Heading Ki:", heading_pid[1])
    print("Heading Kd:", heading_pid[2])

    drive_base.stop()


# Only happens when this file is uploaded by itself. The menu in main.py skips
# this and calls run() instead.
if __name__ == "__main__":
    from helpers import run_alone
    run_alone(run)

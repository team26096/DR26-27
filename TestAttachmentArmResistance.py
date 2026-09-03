"""Gently raise one attachment arm until it meets resistance."""

from pybricks.hubs import PrimeHub
from pybricks.parameters import Port
from pybricks.pupdevices import Motor
from pybricks.tools import wait


# This project normally uses port B for the right/main attachment arm.
ARM_PORT = Port.B

# Gear train used by the attachment motors in the current robot programs.
ARM_GEARS = [[20, 12], [12, 36], [12, 20]]

# Positive speed should move the arm up. Change this to -150 if it moves down.
UP_SPEED_DEGREES_PER_SECOND = 150

# Use only part of the motor's normal maximum torque so a stall is gentle. If
# normal friction makes it stop too soon, increase this a little at a time.
TORQUE_LIMIT_PERCENT = 20

# Print a new measurement ten times per second.
MEASUREMENT_INTERVAL_MS = 100


hub = PrimeHub()
attachment_arm = Motor(ARM_PORT, gears=ARM_GEARS)
normal_speed_limit, normal_acceleration_limit, normal_torque_limit = (
    attachment_arm.control.limits()
)
test_torque_limit = max(
    1,
    normal_torque_limit * TORQUE_LIMIT_PERCENT // 100,
)

try:
    print("Raising attachment arm...")
    print("angle_deg, speed_deg_s, load_mNm, stalled")

    attachment_arm.control.limits(
        normal_speed_limit,
        normal_acceleration_limit,
        test_torque_limit,
    )
    attachment_arm.run(UP_SPEED_DEGREES_PER_SECOND)

    while True:
        angle = attachment_arm.angle()
        speed = attachment_arm.speed()
        load = attachment_arm.load()
        is_stalled = attachment_arm.stalled()

        print(angle, speed, load, is_stalled)

        if is_stalled:
            break

        wait(MEASUREMENT_INTERVAL_MS)

    attachment_arm.brake()
    print("TRIGGERED: resistance detected at", angle, "degrees.")
finally:
    # Also stop safely if the center button ends the program.
    attachment_arm.brake()

    # Put the normal motor limits back for interactive testing afterward.
    attachment_arm.control.limits(
        normal_speed_limit,
        normal_acceleration_limit,
        normal_torque_limit,
    )

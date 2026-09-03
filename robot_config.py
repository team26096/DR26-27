"""Shared settings for our LEGO SPIKE Prime robot."""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase


# Each wheel measures 62.4 millimeters across its center.
WHEEL_DIAMETER_MM = 62.4

# The centers of the left and right wheels are 164 millimeters apart.
AXLE_TRACK_MM = 164

# The robot normally drives straight at 300 millimeters per second.
STRAIGHT_SPEED_MM_PER_SECOND = 300

# The straight speed can change by 600 millimeters per second each second.
STRAIGHT_ACCELERATION_MM_PER_SECOND_SQUARED = 600

# The robot normally turns at 200 degrees per second.
TURN_RATE_DEGREES_PER_SECOND = 200

# The turn speed can change by 400 degrees per second each second.
TURN_ACCELERATION_DEGREES_PER_SECOND_SQUARED = 400


def create_robot():
    """Build the hub, drive motors, and drive base using our shared settings."""

    hub = PrimeHub()

    # Port A controls the left wheel. Counterclockwise makes it drive forward.
    left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)

    # Port E controls the right wheel. Clockwise makes it drive forward.
    right_motor = Motor(Port.E, Direction.CLOCKWISE)

    drive_base = DriveBase(
        left_motor,
        right_motor,
        wheel_diameter=WHEEL_DIAMETER_MM,
        axle_track=AXLE_TRACK_MM,
    )

    # The gyro helps the robot drive straight and make accurate turns.
    drive_base.use_gyro(True)

    # Give every mission the same starting speeds and accelerations.
    drive_base.settings(
        straight_speed=STRAIGHT_SPEED_MM_PER_SECOND,
        straight_acceleration=STRAIGHT_ACCELERATION_MM_PER_SECOND_SQUARED,
        turn_rate=TURN_RATE_DEGREES_PER_SECOND,
        turn_acceleration=TURN_ACCELERATION_DEGREES_PER_SECOND_SQUARED,
    )

    return hub, drive_base, left_motor, right_motor

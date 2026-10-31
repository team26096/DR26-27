# HELPERS FOR OUR SPIKE PRIME ROBOT
# Sets up the hub and motors, and holds the helper code main.py uses.
# You should not need to change this file. Settings are in config.py.

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

import config


# ===== SETUP (happens once) =====

hub = PrimeHub()

# Drive motors.
left_motor = Motor(config.LEFT_MOTOR_PORT, config.LEFT_MOTOR_DIRECTION)
right_motor = Motor(config.RIGHT_MOTOR_PORT, config.RIGHT_MOTOR_DIRECTION)

# Attachment motors.
attachment_left = Motor(config.ATTACHMENT_LEFT_PORT, gears=config.ATTACHMENT_LEFT_GEARS)
attachment_right = Motor(config.ATTACHMENT_RIGHT_PORT, gears=config.ATTACHMENT_RIGHT_GEARS)

# The drive base moves both wheels together. The gyro keeps it straight.
drive_base = DriveBase(left_motor, right_motor,
                       wheel_diameter=config.WHEEL_DIAMETER,
                       axle_track=config.AXLE_TRACK)
drive_base.use_gyro(True)

# Pybricks' own values for this robot, saved before anything changes them.
default_settings = drive_base.settings()
default_heading_pid = drive_base.heading_control.pid()


# ===== HELPERS =====

def reset_robot():
    """Get the robot ready before every run."""
    # Starting speeds and PID, in case the last run changed them.
    drive_base.settings(straight_speed=config.STRAIGHT_SPEED,
                        straight_acceleration=config.STRAIGHT_ACCELERATION,
                        turn_rate=config.TURN_RATE,
                        turn_acceleration=config.TURN_ACCELERATION)
    drive_base.heading_control.pid(*default_heading_pid)

    # Wait for the robot to sit still, so the gyro settles.
    settle_timer = StopWatch()
    while not hub.imu.stationary() and settle_timer.time() < config.SETTLE_TIMEOUT_MS:
        wait(10)

    # Take up gear slack, then zero the arms, heading, and distance.
    # Only this small move is quicker. The run gets the normal acceleration back.
    drive_base.settings(straight_acceleration=config.SLACK_ACCELERATION)
    drive_base.straight(config.SLACK_MM)
    drive_base.stop()
    drive_base.settings(straight_acceleration=config.STRAIGHT_ACCELERATION)
    attachment_left.reset_angle(0)
    attachment_right.reset_angle(0)
    hub.imu.reset_heading(0)
    drive_base.reset()


def battery_level():
    """Return the estimated battery percent and the voltage in mV."""
    voltage = hub.battery.voltage()
    full, empty = config.BATTERY_FULL_MV, config.BATTERY_EMPTY_MV
    percent = (voltage - empty) * 100 / (full - empty)
    return max(0, min(100, round(percent))), voltage


def check_battery(percent):
    if percent < config.LOW_BATTERY_PERCENT:
        print("WARNING: battery is about", percent, "%. Charge it soon.")


def show(label, value):
    """Print one item per line, with the values lined up."""
    print("  " + label + ":" + " " * (18 - len(label)) + value)


def cm(mm):
    return "{:.1f} cm".format(mm / 10)


def sec(ms):
    return "{:.1f} s".format(ms / 1000)


class DistanceTracker:
    """Adds up the total distance of a run, out and back moves included.

    drive_base.distance() only shows how far the robot ended up from the
    start. Run files use this exactly like the normal drive base.
    """

    def __init__(self, drive_base):
        self.drive_base = drive_base
        self.heading_control = drive_base.heading_control
        self.distance_control = drive_base.distance_control
        self.total_mm = 0
        self.last_mm = 0

    def start(self):
        self.total_mm = 0
        self.last_mm = self.drive_base.distance()

    def add_distance(self):
        # Add the distance since the last move. abs() counts backward moves too.
        now = self.drive_base.distance()
        self.total_mm += abs(now - self.last_mm)
        self.last_mm = now

    # Each move first adds up the move before it, then passes the command on.
    def straight(self, *args, **kwargs):
        self.add_distance()
        return self.drive_base.straight(*args, **kwargs)

    def turn(self, *args, **kwargs):
        self.add_distance()
        return self.drive_base.turn(*args, **kwargs)

    def arc(self, *args, **kwargs):
        self.add_distance()
        return self.drive_base.arc(*args, **kwargs)

    def drive(self, *args, **kwargs):
        self.add_distance()
        return self.drive_base.drive(*args, **kwargs)

    def stop(self):
        self.add_distance()
        self.drive_base.stop()

    def brake(self):
        self.add_distance()
        self.drive_base.brake()

    def reset(self, *args, **kwargs):
        self.add_distance()
        self.drive_base.reset(*args, **kwargs)
        # reset() changes distance(), so count from the new value.
        self.last_mm = self.drive_base.distance()

    # These do not move the robot, so they just pass through.
    def settings(self, *args, **kwargs):
        return self.drive_base.settings(*args, **kwargs)

    def distance(self):
        return self.drive_base.distance()

    def angle(self):
        return self.drive_base.angle()


tracker = DistanceTracker(drive_base)

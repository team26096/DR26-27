# HELPERS FOR OUR SPIKE PRIME ROBOT
# Sets up the hub and drive motors, and holds the helper code main.py uses.
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

    # Zero the heading and distance. Each run sets up its own attachments.
    hub.imu.reset_heading(0)
    drive_base.reset()


def run_alone(run):
    """Start one run with no menu, the same way main.py starts it."""
    reset_robot()

    # Same as main.py. Each robot gets its own heading PID.
    if hub.system.info()["name"].lower() == "mickeybricks":
        heading_pid = drive_base.heading_control.pid()
        drive_base.heading_control.pid(23000, *heading_pid[1:])
    elif hub.system.info()["name"].lower() == "pixiebricks":
        heading_pid = drive_base.heading_control.pid()
        drive_base.heading_control.pid(23000, *heading_pid[1:])

    try:
        run(drive_base)
    finally:
        drive_base.stop()


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


def sec(ms):
    return "{:.1f} s".format(ms / 1000)

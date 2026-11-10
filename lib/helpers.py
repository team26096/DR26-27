# HELPERS FOR OUR SPIKE PRIME ROBOT
# Sets up the hub and drive motors, and holds the helper code main.py uses.
# You should not need to change this file. Settings are in lib/config.py.

from pybricks.hubs import PrimeHub
from pybricks.parameters import Color
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# CHANGE (Nov 10): this file and config.py moved to the lib folder. Before, it
# was "import config", and the settings below were written like config.START.
# Now each setting is loaded by name, because the hub can't do
# "import lib.config as config". See the RUNS part of lib/config.py.
from lib.config import (LEFT_MOTOR_PORT, LEFT_MOTOR_DIRECTION,
                        RIGHT_MOTOR_PORT, RIGHT_MOTOR_DIRECTION,
                        WHEEL_DIAMETER, AXLE_TRACK, START, SETTLE_TIMEOUT_MS,
                        BATTERY_FULL_MV, BATTERY_EMPTY_MV, GOOD_BATTERY_PERCENT)


# ===== SETUP (happens once) =====

hub = PrimeHub()

# Drive motors.
left_motor = Motor(LEFT_MOTOR_PORT, LEFT_MOTOR_DIRECTION)
right_motor = Motor(RIGHT_MOTOR_PORT, RIGHT_MOTOR_DIRECTION)

# The drive base moves both wheels together. The gyro keeps it straight.
drive_base = DriveBase(left_motor, right_motor,
                       wheel_diameter=WHEEL_DIAMETER,
                       axle_track=AXLE_TRACK)
drive_base.use_gyro(True)

# Pybricks' own values for this robot, saved before anything changes them.
default_settings = drive_base.settings()
default_heading_pid = drive_base.heading_control.pid()


# ===== HELPERS =====

def reset_robot():
    """Get the robot ready before every run."""
    # Starting speeds and PID, in case the last run changed them.
    # CHANGE (Nov 9): uses START from lib/config.py, the same speeds the runs start with.
    drive_base.settings(**START)
    drive_base.heading_control.pid(*default_heading_pid)

    # Wait for the robot to sit still, so the gyro settles.
    settle_timer = StopWatch()
    while not hub.imu.stationary() and settle_timer.time() < SETTLE_TIMEOUT_MS:
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
    full, empty = BATTERY_FULL_MV, BATTERY_EMPTY_MV
    percent = (voltage - empty) * 100 / (full - empty)
    return max(0, min(100, round(percent))), voltage


# CHANGE (Nov 9): the battery now shows on the center button light, and the
# message is "Charge your robot". Before, it only printed a warning below 30 %.

def battery_light(percent):
    """Turn the center button light green if the battery is good, red if not."""
    if percent > GOOD_BATTERY_PERCENT:
        hub.light.on(Color.GREEN)
    else:
        hub.light.on(Color.RED)


def check_battery(percent):
    """Print a message if the battery needs charging (the same time the light is red)."""
    if percent <= GOOD_BATTERY_PERCENT:
        print("Charge your robot")


def show(label, value):
    """Print one item per line, with the values lined up."""
    print("  " + label + ":" + " " * (18 - len(label)) + value)


def sec(ms):
    return "{:.1f} s".format(ms / 1000)

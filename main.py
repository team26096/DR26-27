# MAIN PROGRAM FOR OUR SPIKE PRIME ROBOT
# Left or right button picks a run. Center button starts it.
# Pressing the center button during a run stops the program.

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, hub_menu
from pybricks import version


# ===== RUN FILES =====
# Each run file has one run() function with only mission moves.
# To add or rename a run, change its import and its line in RUNS.

import run1_fliptherock
import robotrun2
import robotrun3
import robotrun4
import robotrun5
import robotrun6
import robotrun7
import robotrun8

RUNS = {
    "1": run1_fliptherock.run,
    "2": robotrun2.run,
    "3": robotrun3.run,
    "4": robotrun4.run,
    "5": robotrun5.run,
    "6": robotrun6.run,
    "7": robotrun7.run,
    "8": robotrun8.run,
}


# ===== ROBOT SETTINGS (change numbers here only) =====

WHEEL_DIAMETER = 62.4        # mm
AXLE_TRACK = 164             # mm, between the wheel centers

STRAIGHT_SPEED = 400         # mm per second
STRAIGHT_ACCELERATION = 200  # mm per second, each second
TURN_RATE = 200              # degrees per second
TURN_ACCELERATION = 200      # degrees per second, each second

SLACK_MM = -5                # small back up before each run, takes up gear slack

BATTERY_FULL_MV = 8400       # used to estimate the battery percent
BATTERY_EMPTY_MV = 6500
LOW_BATTERY_PERCENT = 30     # print a warning below this


# ===== SETUP (happens once) =====

hub = PrimeHub()

# Drive motors. These directions make positive numbers drive forward.
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E, Direction.CLOCKWISE)

# Attachment motors. The gear list makes angles match the arm, not the motor.
attachment_left = Motor(Port.B, gears=[[12, 20], [12, 12]])
attachment_right = Motor(Port.C, gears=[[12, 20], [12, 12]])

# The drive base moves both wheels together. The gyro keeps it straight.
drive_base = DriveBase(left_motor, right_motor,
                       wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)
drive_base.use_gyro(True)


# ===== HELPERS =====

def reset_robot():
    """Get the robot ready before every run."""
    # Starting speeds, in case the last run changed them.
    drive_base.settings(straight_speed=STRAIGHT_SPEED,
                        straight_acceleration=STRAIGHT_ACCELERATION,
                        turn_rate=TURN_RATE,
                        turn_acceleration=TURN_ACCELERATION)

    # Wait up to 2 seconds for the robot to sit still, so the gyro settles.
    settle_timer = StopWatch()
    while not hub.imu.stationary() and settle_timer.time() < 2000:
        wait(10)

    # Take up gear slack, then zero the arms, heading, and distance.
    drive_base.straight(SLACK_MM)
    drive_base.stop()
    attachment_left.reset_angle(0)
    attachment_right.reset_angle(0)
    hub.imu.reset_heading(0)
    drive_base.reset()


def battery_level():
    """Return the estimated battery percent and the voltage in mV."""
    voltage = hub.battery.voltage()
    percent = (voltage - BATTERY_EMPTY_MV) * 100 / (BATTERY_FULL_MV - BATTERY_EMPTY_MV)
    return max(0, min(100, round(percent))), voltage


def check_battery(percent):
    if percent < LOW_BATTERY_PERCENT:
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

    # These do not move the robot, so they just pass through.
    def settings(self, *args, **kwargs):
        return self.drive_base.settings(*args, **kwargs)

    def distance(self):
        return self.drive_base.distance()


tracker = DistanceTracker(drive_base)


# ===== STARTUP INFO =====

percent, voltage = battery_level()
print("========== ROBOT INFO ==========")
show("Hub name", hub.system.name())
show("Firmware", str(version))
show("Battery", str(percent) + " % (" + str(voltage) + " mV)")
print("================================")
check_battery(percent)

# Session totals. Each run picks up where the last one left off.
runs_done = 0
total_ms = 0
total_mm = 0


# ===== MENU =====

while True:
    # sorted(RUNS) gives "1" to "8", so the menu always matches RUNS.
    choice = hub_menu(*sorted(RUNS))
    hub.display.char(choice)
    print()
    print("Run", choice, "started")

    reset_robot()
    tracker.start()
    start_percent, start_voltage = battery_level()

    # Do the run. The timer starts at 0.
    run_timer = StopWatch()
    RUNS[choice](tracker, attachment_left, attachment_right)
    tracker.stop()
    run_ms = run_timer.time()
    end_percent, end_voltage = battery_level()

    # Add this run to the session totals, remembering where we left off.
    session_start_ms = total_ms
    session_start_mm = total_mm
    runs_done += 1
    total_ms += run_ms
    total_mm += tracker.total_mm

    # This run's results. Net distance is how far it ended from the start.
    print("========== RUN", choice, "RESULTS ==========")
    show("Run time", sec(0) + " to " + sec(run_ms))
    show("Distance", cm(tracker.total_mm))
    show("Net distance", cm(drive_base.distance()))
    show("End heading", "{:.1f} deg".format(hub.imu.heading()))
    show("Left arm", "{:.0f} deg".format(attachment_left.angle()))
    show("Right arm", "{:.0f} deg".format(attachment_right.angle()))
    show("Battery at start", str(start_percent) + " % (" + str(start_voltage) + " mV)")
    show("Battery at end", str(end_percent) + " % (" + str(end_voltage) + " mV)")
    show("Battery drop", str(start_voltage - end_voltage) + " mV")

    # Session totals. These pick up where the last run ended.
    print()
    print("  Session totals after", runs_done, "run(s)")
    show("Total run time", sec(session_start_ms) + " to " + sec(total_ms))
    show("Total distance", cm(session_start_mm) + " to " + cm(total_mm))
    print("========================================")
    check_battery(end_percent)
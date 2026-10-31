# SETTINGS FOR OUR SPIKE PRIME ROBOT
# main.py reads everything from here. Change numbers here, not in main.py.

from pybricks.parameters import Port, Direction


# ===== RUNS =====
# Each run file has one run() function with only mission moves.
# To add or rename a run, change its import and its line in RUNS.

import run1_fliptherock
import run1_researchplatform
import run1_rightbase
import run3_rightbase
import run_forest_elder_seed_collection
import run_explodingseeds
import run_researchplatform

RUNS = {
    "1": run1_fliptherock.run,
    "2": run1_researchplatform.run,
    "3": run1_rightbase.run,
    "4": run3_rightbase.run,
    "5": run_forest_elder_seed_collection.run,
    "6": run_explodingseeds.run,
    "7": run_researchplatform.run,
}


# ===== PORTS =====

# Drive motors. These directions make positive numbers drive forward.
LEFT_MOTOR_PORT = Port.A
LEFT_MOTOR_DIRECTION = Direction.COUNTERCLOCKWISE
RIGHT_MOTOR_PORT = Port.E
RIGHT_MOTOR_DIRECTION = Direction.CLOCKWISE

# Attachment motors. The gear list makes angles match the arm, not the motor.
ATTACHMENT_LEFT_PORT = Port.B
ATTACHMENT_LEFT_GEARS = [[12, 20], [12, 12]]
ATTACHMENT_RIGHT_PORT = Port.C
ATTACHMENT_RIGHT_GEARS = [[12, 20], [12, 12]]


# ===== ROBOT SIZE =====

WHEEL_DIAMETER = 62.4        # mm
AXLE_TRACK = 151            # mm, between the wheel centers


# ===== SPEEDS =====

STRAIGHT_SPEED = 400         # mm per second
STRAIGHT_ACCELERATION = 200  # mm per second, each second
TURN_RATE = 200              # degrees per second
TURN_ACCELERATION = 200      # degrees per second, each second


# ===== BEFORE EACH RUN =====

SETTLE_TIMEOUT_MS = 2000     # wait up to this long for the gyro to settle
SLACK_MM = -5                # small back up before each run, takes up gear slack


# ===== BATTERY =====

BATTERY_FULL_MV = 8400       # used to estimate the battery percent
BATTERY_EMPTY_MV = 6500
LOW_BATTERY_PERCENT = 30     # print a warning below this

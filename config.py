# SETTINGS FOR OUR SPIKE PRIME ROBOT
# main.py reads everything from here. Change numbers here, not in main.py.

from pybricks.parameters import Port, Direction


# ===== RUNS =====
# Each run file has one run() function with only mission moves.
# To add or rename a run, change its import and its line in RUNS.

import run_fliptherock
import run_reachingroots
import run_dronesurvey
import run1_rightbase
import run3_rightbase
import run_forest_elder_seed_collection
import run_explodingseeds
import run_researchplatform
import run_seedsofrenewal

RUNS = {
    "1": run_dronesurvey.run,
    "2": run_fliptherock.run,
    "3": run_reachingroots.run,
    "4": run_researchplatform.run,
    "5": run_explodingseeds.run,
    "6": run3_rightbase.run,
    "7": run1_rightbase.run,
    "8": run_forest_elder_seed_collection.run,
    "9": run_seedsofrenewal.run,
}

# ===== PORTS =====

# Drive motors. These directions make positive numbers drive forward.
LEFT_MOTOR_PORT = Port.A
LEFT_MOTOR_DIRECTION = Direction.COUNTERCLOCKWISE
RIGHT_MOTOR_PORT = Port.E
RIGHT_MOTOR_DIRECTION = Direction.CLOCKWISE

# Attachment ports and gears are set in each run file.


# ===== ROBOT SIZE =====

WHEEL_DIAMETER = 62.4        # mm
AXLE_TRACK = 151            # mm, between the wheel centers


# ===== SPEEDS =====

STRAIGHT_SPEED = 400         # mm per second
STRAIGHT_ACCELERATION = 200  # mm per second, each second
TURN_RATE = 200              # degrees per second
TURN_ACCELERATION = 200      # degrees per second, each second


# ===== BEFORE EACH RUN =====

# The gyro only says "still" after a full second with no bumps, and pressing the
# center button can bump the hub. A short wait can't finish, so it is off. Only
# raise this if runs start crooked.
SETTLE_TIMEOUT_MS = 0        # wait up to this long for the gyro to settle


# ===== BATTERY =====

BATTERY_FULL_MV = 8400       # used to estimate the battery percent
BATTERY_EMPTY_MV = 6500
LOW_BATTERY_PERCENT = 30     # print a warning below this

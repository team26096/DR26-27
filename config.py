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
# CHANGE (Nov 9): one place for the drive speeds. Each run uses START on the way
# out to its mission and FINISH on the way back to base, so you change the speeds
# here and not in every run. Before, every run had its own numbers, and this
# section had STRAIGHT_SPEED = 400, STRAIGHT_ACCELERATION = 200, TURN_RATE = 200
# and TURN_ACCELERATION = 200, used only before each run started.
# A run can still set its own speed for a special move, like a slow push.
#
# The fastest this robot can go is about 550 mm/s straight and about 410 degrees
# per second turning. main.py prints the exact numbers at the start ("Max speed"
# and "Max turn rate"). Stay below them, so the robot has room to correct itself.
#
# Acceleration is how fast the robot speeds up and slows down. Short moves never
# reach full speed, so on those, acceleration saves more time than speed.
# An acceleration can also be two numbers, (speed up, slow down), like (800, 400).
#
# In a run, drive_base.settings(**START) means "use all four START numbers".

# START: driving out to the mission. Slower, so the robot ends up in the right spot.
START = dict(
    straight_speed=350,          # mm per second. Most runs used 300.
    straight_acceleration=600,   # mm per second, each second. Most runs used 400.
    turn_rate=250,               # degrees per second. Runs used 125 to 300.
    turn_acceleration=600,       # degrees per second, each second. Runs used 200 to 500.
)

# FINISH: driving back to base. Faster, because it only has to get home.
FINISH = dict(
    straight_speed=500,          # mm per second. Same as before. Close to the top speed.
    straight_acceleration=1000,  # mm per second, each second. Runs used 800.
    turn_rate=300,               # degrees per second. Runs used 125 to 500.
    turn_acceleration=1000,      # degrees per second, each second. Runs used 400 to 800.
)


# ===== BEFORE EACH RUN =====

# The gyro only says "still" after a full second with no bumps, and pressing the
# center button can bump the hub. A short wait can't finish, so it is off. Only
# raise this if runs start crooked.
SETTLE_TIMEOUT_MS = 0        # wait up to this long for the gyro to settle


# ===== BATTERY =====

BATTERY_FULL_MV = 8400       # used to estimate the battery percent
BATTERY_EMPTY_MV = 6500
# CHANGE (Nov 9): was LOW_BATTERY_PERCENT = 30, which only printed a warning.
# Above this, the center button light is green. At this or below, the light is
# red and "Charge your robot" is printed.
GOOD_BATTERY_PERCENT = 80

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, hub_menu

# Bring in the run files. Each one must be in the same folder as main.py.
# When you add a new run file, remove the # in front of its import line.
import run1_fliptherock
import robotrun2
import robotrun3
import robotrun4
import robotrun5
import robotrun6
import robotrun7
import robotrun8

# Menu number and the run it starts.
# When you add a new run file, also remove the # in front of its line here.
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

# ===== SETUP (happens once) =====

hub = PrimeHub()
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E, Direction.CLOCKWISE)

# Gear list reads from the motor outward and works out to 3 to 1.
attachment_right = Motor(Port.C, gears=[[12, 20], [12, 12]])
attachment_left = Motor(Port.B, gears=[[12, 20], [12, 12]])

# Millimeters.
WHEEL_DIAMETER = 62.4
AXLE_TRACK = 164

drive_base = DriveBase(left_motor, right_motor,
                       wheel_diameter=WHEEL_DIAMETER,
                       axle_track=AXLE_TRACK)

drive_base.use_gyro(True)


# ===== RESET (happens before every run) =====

def reset_robot():
    # Fixed speeds so every run behaves the same.
    # A run can still change them after this.
    drive_base.settings(straight_speed=400, straight_acceleration=200,
                        turn_rate=200, turn_acceleration=200)

    # Takes up slack in the gears.
    drive_base.straight(-5)

    # straight() holds the wheels at the end. Release them before resetting.
    drive_base.stop()

    # Zero everything. Nothing should move the robot after this point.
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)
    attachment_left.reset_angle(0)
    attachment_right.reset_angle(0)
    hub.imu.reset_heading(0)
    drive_base.reset()


# ===== MENU =====
# Left or right button picks a run. Center button starts it.
# The steps below happen for every run, so the run files only hold moves.

while True:
    choice = hub_menu("1", "2", "3", "4", "5", "6", "7", "8")

    # Skip numbers that do not have a run file yet.
    if choice not in RUNS:
        print("Run", choice, "is not added yet")
        continue

    # Hub display: show the run number while the run is going.
    hub.display.char(choice)

    # Console: say which run is starting.
    print("Run", choice, "started")

    reset_robot()

    # TIMER START. A StopWatch counts from the moment it is created.
    run_timer = StopWatch()

    # ---------- RUN ----------
    RUNS[choice](drive_base, attachment_left, attachment_right)

    drive_base.stop()

    # ---------- RESULT ----------

    # TIMER STOP. pause() freezes the value so it cannot creep up after this line.
    run_timer.pause()

    # time() returns milliseconds, so divide by 1000 to get seconds.
    elapsed = round(run_timer.time() / 1000, 1)
    print("Run", choice, "total run time:", elapsed, "seconds")

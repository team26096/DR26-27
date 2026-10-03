from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, hub_menu, StopWatch

# ===== SETUP (happens once) =====

hub = PrimeHub()

left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E, Direction.CLOCKWISE)

drive_base = DriveBase(left_motor, right_motor,
                       wheel_diameter=62.4, axle_track=164)
drive_base.use_gyro(True)

default_settings = drive_base.settings()


def reset_robot():
    drive_base.stop()
    drive_base.settings(*default_settings)
    hub.imu.reset_heading(0)
    drive_base.reset()


# ===== RUN 1 =====

def run1():
    reset_robot()
    # Put run 1 moves here
    drive_base.straight(100)
    drive_base.stop()


# ===== RUN 2 =====

def run2():
    reset_robot()
    # Put run 2 moves here
    drive_base.straight(-100)
    drive_base.stop()


# ===== RUN 3 =====

def run3():
    reset_robot()
    # Put run 3 moves here
    drive_base.straight(100)
    drive_base.stop()


# ===== RUN 4 =====

def run4():
    reset_robot()
    # Put run 4 moves here
    drive_base.straight(100)
    drive_base.stop()


# ===== RUN 5 =====

def run5():
    reset_robot()
    # Put run 5 moves here
    drive_base.straight(100)
    drive_base.stop()


# ===== RUN 6 =====

def run6():
    reset_robot()
    # Put run 6 moves here
    drive_base.straight(100)
    drive_base.stop()


# ===== RUN 7 =====

def run7():
    reset_robot()
    # Put run 7 moves here
    drive_base.straight(100)
    drive_base.stop()


# ===== RUN 8 =====

def run8():
    reset_robot()
    # Put run 8 moves here
    drive_base.straight(100)
    drive_base.stop()


# ===== MENU =====
# Left or right button picks a run. Center button starts it.

while True:
    choice = hub_menu("1", "2", "3", "4", "5", "6", "7", "8")

    # Show the run number on the hub screen while the run is going.
    hub.display.char(choice)

    # Start the timer when the run starts.
    run_timer = StopWatch()

    if choice == "1":
        run1()
    elif choice == "2":
        run2()
    elif choice == "3":
        run3()
    elif choice == "4":
        run4()
    elif choice == "5":
        run5()
    elif choice == "6":
        run6()
    elif choice == "7":
        run7()
    elif choice == "8":
        run8()

    # time() gives milliseconds, so divide by 1000 to get seconds.
    seconds = round(run_timer.time() / 1000, 1)
    print("Run", choice, "took", seconds, "seconds")
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E, Direction.CLOCKWISE)

# Gear list reads from the motor outward and works out to 3 to 1.
attachment_right = Motor(Port.C, gears=[[12, 20], [12, 12]])
attachment_left = Motor(Port.B, gears=[[12, 20], [1, 24]])

# Millimeters.
WHEEL_DIAMETER = 62.4
AXLE_TRACK = 164

drive_base = DriveBase(left_motor, right_motor,
                       wheel_diameter=WHEEL_DIAMETER,
                       axle_track=AXLE_TRACK)
drive_base.use_gyro(True)

# Fixed speeds so every run behaves the same.
drive_base.settings(straight_speed=300, straight_acceleration=600,
                    turn_rate=200, turn_acceleration=400)


# ---------- RESET ----------

# Clear the run time left on the display by the previous run.
hub.display.off()


# Takes up slack in the gears.
drive_base.straight(-10)

# straight() holds the wheels at the end. Release them before resetting.
drive_base.stop()

# Zero everything. Nothing should move the robot after this point.
left_motor.reset_angle(0)
right_motor.reset_angle(0)
attachment_left.reset_angle(0)
attachment_right.reset_angle(0)
hub.imu.reset_heading(0)
drive_base.reset()

# TIMER START. A StopWatch counts from the moment it is created.
run_timer = StopWatch()


# ---------- RUN ----------

attachment_left.run_angle(speed=650, rotation_angle=-90)

drive_base.stop()


# ---------- RESULT ----------

# TIMER STOP. pause() freezes the value so it cannot creep up after this line.
run_timer.pause()

# time() returns milliseconds, so divide by 1000 to get seconds.
elapsed = round(run_timer.time() / 1000, 1)
print("Total run time:", elapsed, "seconds")

# Scrolls about one second per character. Delete if it gets in the way.
hub.display.text(str(elapsed))
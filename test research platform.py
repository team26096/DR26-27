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

hub.display.off()

drive_base.straight(-10)
drive_base.stop()

left_motor.reset_angle(0)
right_motor.reset_angle(0)
attachment_left.reset_angle(0)
attachment_right.reset_angle(0)
hub.imu.reset_heading(0)
drive_base.reset()

run_timer = StopWatch()


# ---------- RUN ----------

# Old single‑motor movement — commented out
# attachment_left.run_angle(speed=650, rotation_angle=-90)

# New: synchronized movement of BOTH drive motors
# Same speed, same angle, same time
left_motor.run_angle(300, 360, wait=False)
right_motor.run_angle(300, 360)

# Repeat as many times as needed
left_motor.run_angle(300, 360, wait=False)
right_motor.run_angle(300, 360)

left_motor.run_angle(300, 360, wait=False)
right_motor.run_angle(300, 360)

drive_base.stop()


# ---------- RESULT ----------

run_timer.pause()

elapsed = round(run_timer.time() / 1000, 1)
print("Total run time:", elapsed, "seconds")

hub.display.text(str(elapsed))

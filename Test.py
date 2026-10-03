from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase

hub = PrimeHub()

left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.B)

drive_base = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=114)

# Main settings
straight_speed, straight_accel, turn_rate, turn_accel = drive_base.settings()

print("Straight speed (mm/s):", straight_speed)
print("Straight acceleration (mm/s^2):", straight_accel)
print("Turn rate (deg/s):", turn_rate)
print("Turn acceleration (deg/s^2):", turn_accel)

# Advanced settings for driving straight
print("Distance limits:", drive_base.distance_control.limits())
print("Distance PID:", drive_base.distance_control.pid())
print("Distance target tolerances:", drive_base.distance_control.target_tolerances())
print("Distance stall tolerances:", drive_base.distance_control.stall_tolerances())

# Advanced settings for turning
print("Heading limits:", drive_base.heading_control.limits())
print("Heading PID:", drive_base.heading_control.pid())
print("Heading target tolerances:", drive_base.heading_control.target_tolerances())
print("Heading stall tolerances:", drive_base.heading_control.stall_tolerances())
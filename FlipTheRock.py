#!/usr/bin/env pybricks-micropython
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase

# Initialize the hub
hub = PrimeHub()

# Initialize left and right motors
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E, Direction.CLOCKWISE)

# Configure the DriveBase
# Measure and adjust these two values (in mm) for your specific build:
WHEEL_DIAMETER = 56  # Standard SPIKE Prime small wheel diameter
AXLE_TRACK = 112     # Distance between the middle of the left and right wheels

drive_base = DriveBase(left_motor, right_motor, wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)

# Use the hub's built-in gyro sensor to prevent drifting while driving
drive_base.use_gyro(True)

# 1. Back into the wall until motors stall (negative speed drives backward)
# drive_power limits motor torque so it stops cleanly against the wall
left_motor.dc(-30)
right_motor.dc(-30)

# Wait until both motors stall against the wall
while not (left_motor.stalled() and right_motor.stalled()):
    pass

# Stop motors after wall alignment
drive_base.stop()

# 2. Reset motor angles and heading back to 0
left_motor.reset_angle(0)
right_motor.reset_angle(0)
hub.imu.reset_heading(0)
drive_base.reset()

# 3. Drive forward 400 mm in a straight line using gyro stabilization
drive_base.straight(400)
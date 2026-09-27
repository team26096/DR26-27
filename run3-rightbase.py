from pybricks.hubs import PrimeHub 
from pybricks.pupdevices import Motor 
from pybricks.parameters import Port, Direction 
from pybricks.robotics import DriveBase 
 
hub = PrimeHub() 
 
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE) 
right_motor = Motor(Port.E, Direction.CLOCKWISE) 
 
drivebase = DriveBase(
    left_motor, 
    right_motor, 
    wheel_diameter=62.4, 
    axle_track=164
) 

drivebase.straight(5) 
drivebase.reset()
drivebase.straight(-650)
print("Distance 1:", drivebase.distance())
drivebase.turn(-62.5)
print("Angle 1:", drivebase.angle())
drivebase.straight(-230) 
print("Distance 2:", drivebase.distance())
# Slow down the turn
drivebase.settings(turn_rate=40)

# See current settings
print(drivebase.heading_control.stall_tolerances())

# Make stall detection less sensitive
drivebase.heading_control.stall_tolerances(
    speed=5,      # must get slower than 5 deg/s
    time=1000     # for 1000 ms before calling it stalled
)

# this is an attempt to turn till the motor stalls insted of turning a fixed angle
# it does not work consistently
# drivebase.drive(0, 30)

# while not drivebase.stalled():
#     pass

# drivebase.stop()

# # drivebase.turn(90)
# print("Angle 2:", drivebase.angle())
#drivebase.turn(-30)
# drivebase.straight(100)


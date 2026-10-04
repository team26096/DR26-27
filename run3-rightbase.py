from pybricks.hubs import PrimeHub 
from pybricks.pupdevices import Motor 
from pybricks.parameters import Port, Direction 
from pybricks.robotics import DriveBase 
from pybricks.tools import StopWatch

timer = StopWatch()
hub = PrimeHub() 
 
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE) 
right_motor = Motor(Port.E, Direction.CLOCKWISE) 
 
drivebase = DriveBase(
    left_motor, 
    right_motor, 
    wheel_diameter=62.4, 
    axle_track=164
) 

drivebase.use_gyro(True)
current_settings = drivebase.settings()
print("Robot Settings:", current_settings)
print("Robot max",drivebase.distance_control.limits())
print("Stall tolerances",drivebase.heading_control.stall_tolerances())

drivebase.settings(900,900,125,200)
drivebase.straight(5) 
drivebase.reset()
drivebase.straight(-540)
drivebase.arc(210, angle=-90)
drivebase.straight(-170)
drivebase.turn(120)

drivebase.drive(-30,0)
while not drivebase.stalled():
    pass
drivebase.stop()

drivebase.arc(10, angle=75)

drivebase.arc(-400, angle=-22) 
drivebase.straight(-200)
drivebase.turn(30)
drivebase.straight(-400)



elapsed_seconds = timer.time() / 1000
print("Elapsed time: {:.2f} seconds".format(elapsed_seconds))

#drivebase.straight(-70)


# print("Distance 1:", drivebase.distance())
# drivebase.turn(-62.5)
# print("Angle 1:", drivebase.angle())
# drivebase.straight(-230) 
# print("Distance 2:", drivebase.distance())
# Slow down the turn
# drivebase.settings(turn_rate=40)

# See current settings

# Make stall detection less sensitive
# drivebase.heading_control.stall_tolerances(
#     speed=5,      # must get slower than 5 deg/s
#     time=1000     # for 1000 ms before calling it stalled
# )

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


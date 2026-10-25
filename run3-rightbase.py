# alignment - right base - left most black bold line - fully visible

from pybricks.hubs import PrimeHub 
from pybricks.pupdevices import Motor 
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase 
from pybricks.tools import StopWatch, wait

timer = StopWatch()
hub = PrimeHub() 
 
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE) 
right_motor = Motor(Port.E, Direction.CLOCKWISE) 
 
drivebase = DriveBase(
    left_motor, 
    right_motor, 
    wheel_diameter=62.4, 
    axle_track=151
) 

drivebase.use_gyro(True)
current_settings = drivebase.settings()
print("Robot Settings:", current_settings)
print("Robot max",drivebase.distance_control.limits())
print("Stall tolerances",drivebase.heading_control.stall_tolerances())

drivebase.settings(500,(800,800),125,500)
drivebase.straight(5) 
drivebase.reset()
drivebase.straight(-510, then=Stop.NONE)
drivebase.arc(210, angle=-90, then=Stop.NONE)
drivebase.straight(-170)
drivebase.turn(130)

drivebase.drive(-50,0)
wait(2500)
#while not drivebase.stalled():
#    pass
drivebase.stop()

drivebase.arc(10, angle=80)
drivebase.arc(-400, distance=-200, then=Stop.NONE)
drivebase.straight(-500)

elapsed_seconds = timer.time() / 1000
print("Elapsed time: {:.2f} seconds".format(elapsed_seconds))

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait


# -------------------------------------------------------------
# 1. Hardware setup
# -------------------------------------------------------------

# Create the hub object.
# This also gives access to the built in gyro, which Pybricks calls the IMU.
hub = PrimeHub()

# Drive motors.
# Direction is chosen so that a positive value moves the robot forward.
# CHECK THIS: your earlier build had left on Port.E and right on Port.A.
# If the robot turns the wrong way, the two ports are swapped.
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E, Direction.CLOCKWISE)

# Attachment motors.
# Uncomment these only if the motors are actually plugged in.
# Creating a Motor on an empty port will raise an error and stop the program.
# arm_motor = Motor(Port.B)
# lift_motor = Motor(Port.C)


# -------------------------------------------------------------
# 2. Robot measurements
# -------------------------------------------------------------

# Wheel diameter in mm.
# 56 mm is the small SPIKE Prime wheel. 62.4 mm is the large one.
# If the robot drives too far, increase this value slightly.
# If it drives too short, decrease it slightly.
WHEEL_DIAMETER = 56

# Axle track in mm. This is the distance between the centers of the two wheels.
# If turns overshoot, reduce this value. If turns undershoot, increase it.
AXLE_TRACK = 164

drive_base = DriveBase(
    left_motor,
    right_motor,
    wheel_diameter=WHEEL_DIAMETER,
    axle_track=AXLE_TRACK,
)

# Use the gyro so the robot holds a straight line and turns accurately.
drive_base.use_gyro(True)


# -------------------------------------------------------------
# 3. Start of run reset
# -------------------------------------------------------------

def reset_everything():
    """Put the robot back into a known starting state.

    Call this once at the very start of every run, with the robot
    sitting still in base and nobody touching it.
    """

    # Stop any leftover movement from a previous run.
    drive_base.stop()

    # The gyro cannot be trusted until it has finished calibrating.
    # hub.imu.ready() becomes True once it is done.
    # If your Pybricks version does not have ready(), delete this loop
    # and use a plain wait(2000) instead.
    while not hub.imu.ready():
        wait(10)

    # Wait until the robot is completely still, up to 3 seconds.
    # If someone is still holding the robot, the heading reset will be off.
    for _ in range(300):
        if hub.imu.stationary():
            break
        wait(10)

    # Send the attachment motors back to their home position.
    # Uncomment the pair that matches how your attachments are built.
    #
    # Option A: the arm has a hard mechanical stop.
    # It runs gently against that stop and calls that position zero.
    # arm_motor.run_until_stalled(-200, then=Stop.HOLD, duty_limit=40)
    # arm_motor.reset_angle(0)
    #
    # Option B: the arm has no hard stop, so just return it to angle zero.
    # arm_motor.run_target(300, 0)

    # Set both drive motor counters back to zero.
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)

    # Set the gyro heading back to zero.
    # Whatever way the robot is pointing right now becomes 0 degrees.
    hub.imu.reset_heading(0)

    # Set the DriveBase distance and angle counters back to zero.
    # Do this last, after the heading reset.
    drive_base.reset()

    # Short pause so everything settles before the first move.
    wait(100)


def return_to_start():
    """Drive back to where the run began.

    This only works if the run was a straight line with no turns.
    drive_base.distance() is how far the robot has moved since the
    last reset, so driving that far in reverse undoes it.
    """
    drive_base.straight(-drive_base.distance())


# Reset first, before the robot moves at all.
reset_everything()

# Drive forward 400 mm. The gyro keeps the line straight.
drive_base.straight(300)

# Drive backward 100 mm. A negative value means reverse.

drive_base.straight(-200)
drive_base.stop()
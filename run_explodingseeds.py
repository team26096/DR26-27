from pybricks.parameters import Port, Stop
from pybricks.pupdevices import Motor
from pybricks.tools import StopWatch


# Exploding Seeds merged run:
# - Runs the existing Exploding Seeds mission first.
# - Runs the tested stall and drive sequence at the end.
#
# This is a separate run file. It is not added to config.RUNS yet.

LEFT_ATTACHMENT_GEARS = [[12, 20], [12, 36]]
RIGHT_ATTACHMENT_GEARS = [[12, 20], [12, 20]]


def run(drive_base):
    attachment_left = None
    attachment_right = None

    try:
        watch = StopWatch()

        # Loaded here because config.py imports this file first.
        from config import START, FINISH

        drive_base.settings(**START)

        attachment_right = Motor(Port.C, gears=RIGHT_ATTACHMENT_GEARS)
        attachment_left = Motor(Port.B, gears=LEFT_ATTACHMENT_GEARS)

        drive_base.straight(-10)
        drive_base.reset()

        # Existing Exploding Seeds mission.

        # Drive forward from base to start aligning with Exploding Seeds.
        drive_base.straight(150)

        # Lift the left arm until it stalls, to set up for Biocentric Architecture.
        attachment_left.run_until_stalled(-170, then=Stop.HOLD, duty_limit=20)
        attachment_left.reset_angle(0)
        attachment_left.run_angle(60, 40, then=Stop.HOLD, wait=False)

        # Turn to keep aligning with Exploding Seeds.
        drive_base.turn(45)
        drive_base.straight(340)

        # Lift the right arm to align for seed removal.
        attachment_right.run_angle(speed=200, rotation_angle=-15)
        drive_base.settings(straight_speed=100)

        # Lift the arm slightly and back up, twice, to get the seed out.
        attachment_right.run_angle(speed=50, rotation_angle=-15)
        drive_base.straight(-18)
        attachment_right.run_angle(speed=25, rotation_angle=-15)
        drive_base.straight(-25)
        attachment_right.run_angle(speed=15, rotation_angle=-15) # speed was 10

        #drive_base.settings(**START)

        drive_base.settings(
             straight_speed=350,
             straight_acceleration=(600,400),
             turn_rate=150,
             turn_acceleration=200,
         )

        drive_base.straight(-100) # used to be -150
        drive_base.arc(-75, -45)
        drive_base.straight(530)
        #drive_base.straight(130) # was 170
        drive_base.arc(75, -27)

        # Tested sequence at the end.
   
        drive_base.straight(70) # was 120

        #wait(5000)
        attachment_left.run_target(30,10)
        attachment_left.run_target(45,40)
        
        drive_base.turn(-10)
        drive_base.straight(50)
        attachment_left.run_target(45,60)
        drive_base.straight(50)

        attachment_right.run_angle(speed=100, rotation_angle=30, wait=True) # speed was 10
        
        drive_base.arc(-75, -35)

        # attachment_left.run_angle(speed=100, rotation_angle=-150) # speed was 10

        drive_base.straight(200)

        drive_base.arc(-75, 45)

        drive_base.straight(25)

        attachment_right.run_angle(speed=100, rotation_angle=-30) # speed was 10


    
        drive_base.settings(**FINISH)
        drive_base.straight(-50)

        drive_base.turn(70)

        drive_base.straight(650)


        print("Merged Exploding Seeds run complete.")
        print("Elapsed seconds:", watch.time() / 1000)

        # Save the final angles before releasing the attachment ports.
        return (attachment_left.angle(), attachment_right.angle())

    finally:
        if attachment_left is not None:
            attachment_left.close()
        if attachment_right is not None:
            attachment_right.close()


if __name__ == "__main__":
    from helpers import run_alone

    run_alone(run)

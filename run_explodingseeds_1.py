from pybricks.parameters import Port, Stop
from pybricks.pupdevices import Motor
from pybricks.tools import StopWatch

def run(drive_base):
   attachment_left = None
   attachment_right = None
   try:
       # Exploding Seeds, Biocentric Architecture, and Window to the Past.
       # Same moves as ExplodingSeeds.py.

       watch = StopWatch()

       # Loaded here, not at the top, because lib/config.py loads this file first.
       from lib.config import START, FINISH

       # Start speeds from lib/config.py. The straight speed changes further down
       # are part of the mission, so they stay in this file.
       # CHANGE (Nov 9): was straight_speed=300, straight_acceleration=400, with
       # Pybricks' own turn speeds (default_settings[2] and [3]), because
       # ExplodingSeeds.py only set the straight speed.
       drive_base.settings(**START)


       # Attachment gears from ExplodingSeeds.py, for this run only.
       attachment_right = Motor(Port.C, gears=[[12,20],[12,20]])
       attachment_left = Motor(Port.B, gears=[[12,20],[12,36]])


       drive_base.straight(-10)
       drive_base.reset()
       print(drive_base.angle())

       # Drive forward from base to start aligning with Exploding Seeds.
       drive_base.straight(150)

       # Lift the left arm until it stalls, to set up for Biocentric Architecture.
       attachment_left.run_until_stalled(-170, then=Stop.HOLD, duty_limit=20)

       # Turn to keep aligning with Exploding Seeds.
       drive_base.turn(45)    
       drive_base.straight(340)

       # Lift the right arm to align for seed removal.
       attachment_right.run_angle(speed=200, rotation_angle=20)
       drive_base.settings(straight_speed=100)

       # Lift the arm slightly and back up, twice, to get the seed out.
       attachment_right.run_angle(speed=50, rotation_angle=5)
       drive_base.straight(-18)
       attachment_right.run_angle(speed=25, rotation_angle=5)
       drive_base.straight(-15)
       attachment_right.run_angle(speed=10, rotation_angle=30)

       drive_base.settings(straight_speed=300)
       drive_base.straight(-150)
       drive_base.arc(-75, -45)
       drive_base.straight(400)

       attachment_left.run_angle(speed=200, rotation_angle=140, wait=True)
       drive_base.straight(170)

       # Arm up to complete the nesting canopy.
       attachment_left.run_angle(speed=25, rotation_angle=-40)

       # Arm down again to make sure the compost hatch is complete.
       attachment_left.run_angle(speed=100, rotation_angle=35)

       drive_base.arc(75, -27)

       attachment_left.run_angle(speed=500, rotation_angle=-90)
       attachment_right.run_angle(speed=200, rotation_angle=-30)
       drive_base.straight(370)
       attachment_right.run_angle(speed=300, rotation_angle=50)

       # Save the final angles before releasing the attachment ports.
       return (attachment_left.angle(), attachment_right.angle())
   finally:
       if attachment_left is not None:
           attachment_left.close()
       if attachment_right is not None:
           attachment_right.close()

# Only happens when this file is started by itself. The menu in main.py skips
# this and calls run() instead.
# CHANGE (Nov 10): this file moved to the runs folder. Started from here, it
# can't load lib/helpers.py, because the hub only gets the files it can find
# next to the file you start. To test this run by itself, start test_run.py in
# the main folder. Before, this part started the run with run_alone().
if __name__ == "__main__":
   print("To test this run by itself, start test_run.py in the main folder.")


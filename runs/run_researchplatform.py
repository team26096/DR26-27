from pybricks.parameters import Port, Stop
from pybricks.pupdevices import Motor
from pybricks.tools import wait, StopWatch


def run(drive_base):
    attachment_left = None
    attachment_right = None
    try:
        # Research Platform. Same code as ResearchPlatform.py.

        # Loaded here, not at the top, because lib/helpers.py needs lib/config.py to finish first.
        from lib.helpers import hub

        watch = StopWatch()

        # Attachment motors setup
        attachment_right = Motor(Port.C, gears=[[12,20],[12,20]])
        attachment_left = Motor(Port.B, gears=[[12,20]])

        # Loaded here, not at the top, because lib/config.py loads this file first.
        from lib.config import START, FINISH

        # Start speeds from lib/config.py.
        # CHANGE (Nov 9): was straight_speed=300, straight_acceleration=400,
        # turn_rate=200, turn_acceleration=200.
        drive_base.settings(**START)

        # left_motor.reset_angle(0)
        hub.imu.reset_heading(0)

        # Takes up slack in the gears.
        drive_base.straight(-10)

        drive_base.reset()
        # Start the arm moving, then drive at the same time (wait=False doesn't block).
        attachment_right.run_angle(speed=600, rotation_angle=-90, then=Stop.HOLD, wait=False)
        drive_base.straight(570)
        drive_base.arc(10,90)
        drive_base.straight(190)
        drive_base.arc(-82, angle=90)

        #Tangled Start
        # This speed stays here, not in lib/config.py, because it is part of the
        # mission, not the way out or back.
        drive_base.settings(straight_speed=500, straight_acceleration=(800),
                            turn_rate=200, turn_acceleration=200)

        drive_base.straight(70)
        #attachment_left.run_angle(speed=600, rotation_angle=45, wait=False) 
        attachment_right.run_angle(speed=600, rotation_angle=90, then=Stop.HOLD)
        attachment_right.run_angle(speed=600, rotation_angle=-90, then=Stop.HOLD) 
        drive_base.straight(70, wait=False) 
        timer = StopWatch()
        while not drive_base.done():
            if timer.time() > 1000:
                drive_base.stop() 
                print("TIMED OUT")
                break
            wait(10)
        drive_base.straight(-130) #changed after new attachment


        #attachment_right.run_angle(speed=600, rotation_angle=60, then=Stop.HOLD)
        drive_base.arc(82, angle=-90)

        start = drive_base.distance()
        drive_base.straight(-220, wait=False) 
        timer = StopWatch() 
        while not drive_base.done():
            if timer.time() > 1000:
                drive_base.stop()
                print("TIMED OUT")
                break
            wait(10)

        # Finish speeds from lib/config.py.
        # CHANGE (Nov 9): was straight_speed=500, straight_acceleration=800,
        # turn_rate=200, turn_acceleration=200.
        drive_base.settings(**FINISH)
    
        drive_base.straight(150, then=Stop.NONE)
        drive_base.arc(-450,distance=750)
        drive_base.stop()

        # TIMER STOP. pause() freezes the value so it cannot creep up after this line.
        watch.pause()

        # time() returns milliseconds, so divide by 1000 to get seconds.
        elapsed = round(watch.time() / 1000, 1)
        print("Total run time:", elapsed, "seconds")

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
from pybricks.parameters import Port, Stop
from pybricks.pupdevices import Motor
from pybricks.tools import StopWatch


def run(drivebase):
    motor_left = None
    motor_right = None
    try:
        # Forest Elder seed collection. Same code as forest_elder_seed_collection.py.

        # Loaded here, not at the top, because lib/helpers.py needs lib/config.py to finish first.
        from lib.helpers import default_settings, hub

        voltage = hub.battery.voltage()
        print("Battery Voltage:", voltage, "mV")

        # Attachment motor
        motor_right = Motor(
            Port.C,
            gears=[
                [12, 20]
            ]
        )

        motor_left = Motor(
            Port.B,
            gears=[
                [12, 20],
                [12, 36]
            ]
        )

        # forest_elder_seed_collection.py only set the straight speeds, so its turns
        # used Pybricks' own speeds and not the ones in lib/config.py.
        drivebase.settings(turn_rate=default_settings[2],
                           turn_acceleration=default_settings[3])

        # Make straight driving faster
        drivebase.settings(
            straight_speed=500,         # mm/s
            straight_acceleration=400  # mm/s^2
        )

        current_settings = drivebase.settings()
        print("Robot Settings:", current_settings)

        # TIMER START. A StopWatch counts from the moment it is created.
        run_timer = StopWatch()

        # Takes up slack in the gears.
        drivebase.straight(-10)

        motor_right.run_until_stalled(200, then=Stop.HOLD, duty_limit=25 )
        # motor_left.run_until_stalled(200, then=Stop.HOLD, duty_limit=25 )
        # motor_left.reset_angle(0)
        #  motor_left.run_angle(
        #     speed=200,
        #     rotation_angle=-50,
        #     then=Stop.HOLD,
        #     wait=True
        # )
        # 1. Drive forward 50 cm = 500 mm
        drivebase.straight(410)
        drivebase.stop()
        drivebase.reset()

        # 2. Rotate the entire robot 30 degrees
        drivebase.turn(37)

        drivebase.straight(112)

        motor_left.run_angle(
            speed=90,
            rotation_angle=35,
            then=Stop.HOLD,
            wait=True
        )

        # # 4. Rotate Motor C 45 degrees2
        motor_right.run_angle(
            speed=200,
            rotation_angle=-50,
            then=Stop.HOLD,
            wait=True
        )

        drivebase.straight(-160)

        motor_right.run_angle(
            speed=200,
            rotation_angle=30,
            then=Stop.HOLD,
            wait=True
        )

        drivebase.straight(-120)
        drivebase.turn(-12)
        # drivebase.straight(-25)
        drivebase.turn(-80)
        drivebase.straight(-350)
        # drivebase.stop()

        # ---------- RESULT ----------

        # # TIMER STOP. pause() freezes the value so it cannot creep up after this line.
        run_timer.pause()

        # # time() returns milliseconds, so divide by 1000 to get seconds.
        elapsed = round(run_timer.time() / 1000, 1)
        print("Total run time:", elapsed, "seconds")

        # Save the final angles before releasing the attachment ports.
        return (motor_left.angle(), motor_right.angle())
    finally:
        if motor_left is not None:
            motor_left.close()
        if motor_right is not None:
            motor_right.close()


# Only happens when this file is started by itself. The menu in main.py skips
# this and calls run() instead.
# CHANGE (Nov 10): this file moved to the runs folder. Started from here, it
# can't load lib/helpers.py, because the hub only gets the files it can find
# next to the file you start. To test this run by itself, start test_run.py in
# the main folder. Before, this part started the run with run_alone().
if __name__ == "__main__":
    print("To test this run by itself, start test_run.py in the main folder.")

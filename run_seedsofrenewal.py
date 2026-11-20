from pybricks.parameters import Port, Stop
from pybricks.pupdevices import Motor
from pybricks.tools import StopWatch


def run(drivebase):
    motor_right = None
    try:
        # Seeds of Renewal. Same code as seedsofrenewal.py.

        # Loaded here, not at the top, because helpers.py needs config.py to finish first.
        from helpers import hub

        voltage = hub.battery.voltage()
        print("Battery Voltage:", voltage, "mV")

        # Attachment motor
        motor_left = Motor(
            Port.B,
            gears=[
                [12, 20],[1, 8]
            ]
        )

        # seedsofrenewal.py used axle_track=160 and config.py has 151. That only
        # changes turns, and this run has none.

        # Make straight driving faster
        drivebase.settings(
            straight_speed=500,         # mm/s
            straight_acceleration=(800,400)  # mm/s^2
        )

        current_settings = drivebase.settings()
        print("Robot Settings:", current_settings)

        # TIMER START. A StopWatch counts from the moment it is created.
        run_timer = StopWatch()
        drivebase.straight(240)
        motor_left.run_angle(
            speed=90,
            rotation_angle=-40,
            then=Stop.HOLD,
            wait=True
        )
        # # TIMER STOP. pause() freezes the value so it cannot creep up after this line.
        run_timer.pause()

        # # time() returns milliseconds, so divide by 1000 to get seconds.
        elapsed = round(run_timer.time() / 1000, 1)
        print("Total run time:", elapsed, "seconds")

        # Save the final angles before releasing the attachment ports.
        return (None, motor_left.angle())
    finally:
        if motor_right is not None:
            motor_right.close()


# Only happens when this file is uploaded by itself. The menu in main.py skips
# this and calls run() instead.
if __name__ == "__main__":
    from helpers import run_alone
    run_alone(run)

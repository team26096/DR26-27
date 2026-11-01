from pybricks.parameters import Port, Stop
from pybricks.pupdevices import Motor
from pybricks.tools import StopWatch


def run(drivebase, attachment_left, attachment_right):
    # Forest Elder seed collection. Same code as forest_elder_seed_collection.py.

    # Loaded here, not at the top, because helpers.py needs config.py to finish first.
    import config
    from helpers import default_settings, hub

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
    # used Pybricks' own speeds and not the ones in config.py.
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

    # Put back the gears from config.py. The arms in main.py use the same motors,
    # so without this every run after this one would get the gears from above.
    Motor(config.ATTACHMENT_LEFT_PORT, gears=config.ATTACHMENT_LEFT_GEARS)
    Motor(config.ATTACHMENT_RIGHT_PORT, gears=config.ATTACHMENT_RIGHT_GEARS)

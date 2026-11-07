# MAIN PROGRAM FOR OUR SPIKE PRIME ROBOT
# Left or right button picks a run. Center button starts it.
# After a run, the menu moves on to the next run and waits for the center button.
# Pressing the center button during a run stops the program.
# Settings and the list of runs are in config.py. Setup and helpers are in
# helpers.py. This file stays the same.

from pybricks.tools import StopWatch, hub_menu
from pybricks import version

import config
from helpers import (hub, drive_base,
                     reset_robot, battery_level, check_battery, show, sec)

# ===== STARTUP INFO =====

percent, voltage = battery_level()
print("========== ROBOT INFO ==========")
show("Hub name", hub.system.name())
show("Firmware", str(version))
show("Battery", str(percent) + " % (" + str(voltage) + " mV)")
print("================================")
check_battery(percent)

# ===== MENU =====

# sorted() lists the run numbers in order, so the menu always matches RUNS.
run_numbers = sorted(config.RUNS)
next_index = 0

# CHANGE (Nov 5): the results now also show transition times. A transition is
# the time between one run ending and the next run starting. Before, this file
# kept a list of run times and used a second timer for the total. Now one clock
# measures everything, so the run times plus the transition times always add up
# to the total time.

# Every run so far, in the order they ran, as
# (run before it, run, transition time before it, run time).
# The first run has no run or transition before it.
history = []
total_run_ms = 0
total_transition_ms = 0

# One clock for all runs. It starts with the first run. Run times and transition
# times both come from it, so they always add up to the total time.
match_timer = StopWatch()
last_end_ms = 0

while True:
    # hub_menu always opens on the first item, so put the next run first.
    choice = hub_menu(*(run_numbers[next_index:] + run_numbers[:next_index]))
    hub.display.char(choice)
    print()
    print("Run", choice, "started")

    reset_robot()

    # Each robot gets its own heading PID. Change one robot's number without
    # touching the other's.
    # This goes after reset_robot(), which puts the default PID back before every run.
    if hub.system.info()["name"].lower() == "mickeybricks":
        heading_pid = drive_base.heading_control.pid()
        drive_base.heading_control.pid(23000, *heading_pid[1:])
    elif hub.system.info()["name"].lower() == "pixiebricks":
        heading_pid = drive_base.heading_control.pid()
        drive_base.heading_control.pid(23000, *heading_pid[1:])

    start_percent, start_voltage = battery_level()

    # The clock starts with the first run.
    if not history:
        match_timer.reset()
    start_ms = match_timer.time()

    # Transition: from the moment the last run stopped until this run starts.
    # It covers moving the robot, the menu, and the setup above.
    if history:
        previous = history[-1][1]
        transition_ms = start_ms - last_end_ms
    else:
        previous = None
        transition_ms = None

    # Do the run.
    try:
        arm_angles = config.RUNS[choice](drive_base)
    finally:
        drive_base.stop()
    last_end_ms = match_timer.time()
    run_ms = last_end_ms - start_ms
    end_percent, end_voltage = battery_level()

    # A repeated run counts again, because it really took that time.
    history.append((previous, choice, transition_ms, run_ms))
    total_run_ms += run_ms
    if transition_ms is not None:
        total_transition_ms += transition_ms

    # The menu opens on the run after this one. After the last run, back to the first.
    next_index = (run_numbers.index(choice) + 1) % len(run_numbers)

    # Show it now. With a computer connected, the printing below can take a moment.
    hub.display.char(run_numbers[next_index])

    # This run's results.
    # CHANGE (Nov 5): added the transition line. The line that used to say
    # "Total run time" is now called "Run time".
    print("========== RUN", choice, "RESULTS ==========")
    if transition_ms is not None:
        show("Transition " + previous + " -> " + choice, sec(transition_ms))
    show("Run time", sec(run_ms))
    show("End heading", "{:.1f} deg".format(hub.imu.heading()))
    if arm_angles is not None:
        for label, angle in zip(("Left arm", "Right arm"), arm_angles):
            if angle is not None:
                show(label, "{:.0f} deg".format(angle))
    show("Battery at start", str(start_percent) + " % (" + str(start_voltage) + " mV)")
    show("Battery at end", str(end_percent) + " % (" + str(end_voltage) + " mV)")
    show("Battery drop", str(start_voltage - end_voltage) + " mV")
    print("========================================")

    # Every run and transition in order. After the last run, this has the final totals.
    # CHANGE (Nov 5): transitions are now listed between the runs. "Time running"
    # is now called "Total run time", "With time between" is now "Total time",
    # and "Total transition" is new.
    print("========== ALL RUNS SO FAR ==========")
    for before, number, transition, ms in history:
        if before is not None:
            show("Transition " + before + " -> " + number, sec(transition))
        show("Run " + number, sec(ms))
    print("  ----------------------------------")
    show("Total run time", sec(total_run_ms))
    show("Total transition", sec(total_transition_ms))
    show("Total time", sec(last_end_ms))
    print("========================================")
    check_battery(end_percent)
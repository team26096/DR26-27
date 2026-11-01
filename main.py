# MAIN PROGRAM FOR OUR SPIKE PRIME ROBOT
# Left or right button picks a run. Center button starts it.
# After a run, the menu moves on to the next run and waits for the center button.
# Pressing the center button during a run stops the program.
# Settings and the list of runs are in config.py. Setup and helpers are in
# helpers.py. This file stays the same.

from pybricks.tools import StopWatch, hub_menu
from pybricks import version

import config
from helpers import (hub, drive_base, attachment_left, attachment_right,
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

# Every run so far, in the order they ran.
run_times = []
total_ms = 0
all_runs_timer = StopWatch()

while True:
    # hub_menu always opens on the first item, so put the next run first.
    choice = hub_menu(*(run_numbers[next_index:] + run_numbers[:next_index]))
    hub.display.char(choice)
    print()
    print("Run", choice, "started")

    reset_robot()

    # PixieBricks keeps its original hub PID defaults; only MickeyBricks is tuned.
    # This goes after reset_robot(), which puts the default PID back before every run.
    if hub.system.info()["name"].lower() == "mickeybricks":
        heading_pid = drive_base.heading_control.pid()
        drive_base.heading_control.pid(23000, *heading_pid[1:])

    start_percent, start_voltage = battery_level()

    # The timer for all runs starts with the first run.
    if not run_times:
        all_runs_timer.reset()

    # Do the run. The timer starts at 0.
    run_timer = StopWatch()
    config.RUNS[choice](drive_base, attachment_left, attachment_right)
    drive_base.stop()
    run_ms = run_timer.time()
    all_runs_ms = all_runs_timer.time()
    end_percent, end_voltage = battery_level()

    # A repeated run counts again, because it really took that time.
    run_times.append((choice, run_ms))
    total_ms += run_ms

    # The menu opens on the run after this one. After the last run, back to the first.
    next_index = (run_numbers.index(choice) + 1) % len(run_numbers)

    # Show it now. With a computer connected, the printing below can take a moment.
    hub.display.char(run_numbers[next_index])

    # This run's results.
    print("========== RUN", choice, "RESULTS ==========")
    show("Total run time", sec(run_ms))
    show("End heading", "{:.1f} deg".format(hub.imu.heading()))
    show("Left arm", "{:.0f} deg".format(attachment_left.angle()))
    show("Right arm", "{:.0f} deg".format(attachment_right.angle()))
    show("Battery at start", str(start_percent) + " % (" + str(start_voltage) + " mV)")
    show("Battery at end", str(end_percent) + " % (" + str(end_voltage) + " mV)")
    show("Battery drop", str(start_voltage - end_voltage) + " mV")
    print("========================================")

    # After the last run, this has the final totals.
    print("========== ALL RUNS SO FAR ==========")
    for number, ms in run_times:
        show("Run " + number, sec(ms))
    show("Time running", sec(total_ms))
    show("With time between", sec(all_runs_ms))
    print("========================================")
    check_battery(end_percent)
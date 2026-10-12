# MAIN PROGRAM FOR OUR SPIKE PRIME ROBOT
# Left or right button picks a run. Center button starts it.
# Pressing the center button during a run stops the program.
# Settings and the list of runs are in config.py. Setup and helpers are in
# helpers.py. This file stays the same.

from pybricks.tools import StopWatch, hub_menu
from pybricks import version

import config
from helpers import (hub, drive_base, attachment_left, attachment_right, tracker,
                     reset_robot, battery_level, check_battery, show, cm, sec)

# ===== STARTUP INFO =====

percent, voltage = battery_level()
print("========== ROBOT INFO ==========")
show("Hub name", hub.system.name())
show("Firmware", str(version))
show("Battery", str(percent) + " % (" + str(voltage) + " mV)")
print("================================")
check_battery(percent)

# Session totals. Each run picks up where the last one left off.
runs_done = 0
total_ms = 0
total_mm = 0

# ===== MENU =====

while True:
    # sorted() lists the run numbers in order, so the menu always matches RUNS.
    choice = hub_menu(*sorted(config.RUNS))
    hub.display.char(choice)
    print()
    print("Run", choice, "started")

    reset_robot()
    tracker.start()
    start_percent, start_voltage = battery_level()

    # Do the run. The timer starts at 0.
    run_timer = StopWatch()
    config.RUNS[choice](tracker, attachment_left, attachment_right)
    tracker.stop()
    run_ms = run_timer.time()
    end_percent, end_voltage = battery_level()

    # Add this run to the session totals, remembering where we left off.
    session_start_ms = total_ms
    session_start_mm = total_mm
    runs_done += 1
    total_ms += run_ms
    total_mm += tracker.total_mm

    # This run's results. Net distance is how far it ended from the start.
    print("========== RUN", choice, "RESULTS ==========")
    show("Run time", sec(0) + " to " + sec(run_ms))
    show("Distance", cm(tracker.total_mm))
    show("Net distance", cm(drive_base.distance()))
    show("End heading", "{:.1f} deg".format(hub.imu.heading()))
    show("Left arm", "{:.0f} deg".format(attachment_left.angle()))
    show("Right arm", "{:.0f} deg".format(attachment_right.angle()))
    show("Battery at start", str(start_percent) + " % (" + str(start_voltage) + " mV)")
    show("Battery at end", str(end_percent) + " % (" + str(end_voltage) + " mV)")
    show("Battery drop", str(start_voltage - end_voltage) + " mV")

    # Session totals. These pick up where the last run ended.
    print()
    print("  Session totals after", runs_done, "run(s)")
    show("Total run time", sec(session_start_ms) + " to " + sec(total_ms))
    show("Total distance", cm(session_start_mm) + " to " + cm(total_mm))
    print("========================================")
    check_battery(end_percent)
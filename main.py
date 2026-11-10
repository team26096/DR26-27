 # MAIN  PROGRAM FOR OUR SPIKE PRIME ROBOT
# Left or right button picks a run. Center button starts it.
# After a run, the menu moves on to the next run and waits for the center button.
# After the last run in the menu, the program ends.
# Pressing the center button during a run stops the program.
# Settings and the list of runs are in lib/config.py. Setup and helpers are in
# lib/helpers.py. The runs are in the runs folder. This file stays the same.

from pybricks.tools import StopWatch, hub_menu
from pybricks import version

# CHANGE (Nov 10): config.py and helpers.py moved to the lib folder, and the
# run files moved to the runs folder. Before, it was "import config" and
# "config.RUNS". See the RUNS part of lib/config.py for how to write imports
# that work on the hub.
from lib.config import RUNS
from lib.helpers import (hub, drive_base, reset_robot, battery_level,
                         battery_light, check_battery, show, sec)

# ===== STARTUP INFO =====

start_percent, voltage = battery_level()
print("========== ROBOT INFO ==========")
show("Hub name", hub.system.name())
show("Firmware", str(version))
show("Battery", str(start_percent) + " % (" + str(voltage) + " mV)")
# CHANGE (Nov 9): the fastest this robot can drive and turn, to help pick the
# START and FINISH speeds in lib/config.py.
show("Max speed", str(drive_base.distance_control.limits()[0]) + " mm/s")
show("Max turn rate", str(drive_base.heading_control.limits()[0]) + " deg/s")
print("================================")
# CHANGE (Nov 9): the center button light shows the battery. Green means it is
# above 80 %. Red means charge it, and then "Charge your robot" is printed too.
battery_light(start_percent)
check_battery(start_percent)

# ===== MENU =====

# sorted() lists the run numbers in order, so the menu always matches RUNS.
run_numbers = sorted(RUNS)
next_index = 0

# CHANGE (Nov 5): the results now also show transition times. A transition is
# the time between one run ending and the next run starting. Before, this file
# kept a list of run times and used a second timer for the total. Now one clock
# measures everything, so the run times plus the transition times always add up
# to the total time.

# Every run so far, in the order they ran, as
# (run before it, run, transition time before it, run time, finished).
# The first run has no run or transition before it.
# CHANGE (Nov 9): "finished" is new. It is False if the run was stopped.
history = []
total_run_ms = 0
total_transition_ms = 0

# One clock for all runs. It starts with the first run. Run times and transition
# times both come from it, so they always add up to the total time.
match_timer = StopWatch()
last_end_ms = 0

# ===== SUMMARY =====

# CHANGE (Nov 9): the results of each run are not printed anymore. Only this
# summary of all runs is printed: after the last run in the menu, and when the
# program stops early, like when a run is stopped with the center button.
# Before, "RUN ... RESULTS" and "ALL RUNS SO FAR" were printed after every run.
# To also save the summary in a log file and upload it to GitHub, start the
# program with: python tools/run_logged.py main.py
# The upload happens when the program ends: after the last run, or when it
# is stopped early.

# How many runs the last summary had, so the same summary isn't printed twice.
summary_runs = 0


def print_summary(title):
    global summary_runs
    summary_runs = len(history)
    print()
    print("========== " + title + " ==========")
    for before, number, transition, ms, finished in history:
        if before is not None:
            show("Transition " + before + " -> " + number, sec(transition))
        if finished:
            show("Run " + number, sec(ms))
        else:
            show("Run " + number + " (stopped)", sec(ms))
    print("  ----------------------------------")
    show("Total run time", sec(total_run_ms))
    show("Total transition", sec(total_transition_ms))
    show("Total time", sec(last_end_ms))
    # Runs from the menu that have not finished even once.
    finished_runs = [entry[1] for entry in history if entry[4]]
    not_done = [number for number in run_numbers if number not in finished_runs]
    if not_done:
        show("Not done", ", ".join(not_done))
    end_percent = battery_level()[0]
    show("Battery", str(start_percent) + " % at start, " + str(end_percent) + " % now")
    print("========================================")
    check_battery(end_percent)


# ===== RUNS =====

try:
    while True:
        # hub_menu always opens on the first item, so put the next run first.
        choice = hub_menu(*(run_numbers[next_index:] + run_numbers[:next_index]))
        hub.display.char(choice)

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

        # Do the run. The "finally" part also happens when the run is stopped,
        # so a stopped run still goes in the summary with its time.
        finished = False
        try:
            RUNS[choice](drive_base)
            finished = True
        finally:
            drive_base.stop()
            last_end_ms = match_timer.time()
            run_ms = last_end_ms - start_ms
            # A repeated run counts again, because it really took that time.
            history.append((previous, choice, transition_ms, run_ms, finished))
            total_run_ms += run_ms
            if transition_ms is not None:
                total_transition_ms += transition_ms

        # The menu opens on the run after this one.
        next_index = (run_numbers.index(choice) + 1) % len(run_numbers)
        hub.display.char(run_numbers[next_index])
        battery_light(battery_level()[0])

        # CHANGE (Nov 9): the program ends after the last run in the menu.
        # Before, the menu went back to the first run and the program kept
        # going, so tools/run_logged.py could not upload the log until someone
        # stopped it. Now the log goes up to GitHub right after this summary.
        # To do more runs, start the program again.
        if choice == run_numbers[-1]:
            print_summary("FINAL SUMMARY")
            break

except BaseException:
    # The program is stopping: a run was stopped with the center button, the
    # computer stopped it, or something went wrong. Show where things stand,
    # then let the program stop like before.
    if len(history) > summary_runs:
        print_summary("ALL RUNS SO FAR")
    raise

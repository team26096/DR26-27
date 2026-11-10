# DR26-27
Darth Rappers FLL 26-27 Source Code

## Folders

- `main.py` - the program to start. Pick a run with the left and right buttons.
- `test_run.py` - start this to test one run without the menu.
- `lib/config.py` - settings, speeds, and the list of runs in the menu (`RUNS`).
- `lib/helpers.py` - sets up the robot and holds helper code.
- `runs/` - one file per run, each with a `run()` function.
- `tools/` - scripts that run on the computer, not the hub.

Always start `main.py` or `test_run.py`, not a file in `lib/` or `runs/`.

Write imports from these folders like this, or they stop the program on the hub:

    from runs.run_dronesurvey import run as run_dronesurvey
    from lib.config import START

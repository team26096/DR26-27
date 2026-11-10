# TEST ONE RUN WITHOUT THE MENU
# CHANGE (Nov 10): new file. The run files moved to the runs folder, and a file
# started from there can't load lib/helpers.py. Start this file instead.
# Before, you started the run file itself.
#
# Put the menu number of the run here, from RUNS in lib/config.py. To test a
# run that is not in RUNS yet, add it to RUNS first.
RUN = "1"

from lib.config import RUNS
from lib.helpers import run_alone

run_alone(RUNS[RUN])

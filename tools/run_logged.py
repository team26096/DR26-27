"""Run a hub program and save everything it prints in a log file.

This runs on the computer, not on the hub. It starts the program the same way
as "pybricksdev run ble main.py". The output shows in the terminal like always,
and every line also goes into a new log file in the logs folder. The file name
has the program name and the date and time it started, so every run gets its
own file:

    logs/main_2026-11-09_17-55-03.log

Each line in the log file starts with the time the computer got it.

CHANGE (Nov 9): when the program ends, every log file that is not on GitHub
yet goes up to the logs folder on GitHub, on the main branch. Nothing else is
uploaded. The code on this computer is not committed or pushed, the files are
not changed, and it doesn't matter which branch you are on. If the upload
doesn't work, for example with no internet, the log file is still saved on this
computer and goes up with the next upload that works. The logs folder is in
.gitignore, so git never adds it with the code. "git pull" brings the uploaded
logs back down, and that's fine.

Use it from the robot folder (on a Mac, type python3 instead of python):

    python tools/run_logged.py main.py
    python tools/run_logged.py main.py --name PixieBricks

Anything after the program name goes to pybricksdev unchanged.

CHANGE (Nov 9): the "Run on LEGO Brick" button in VS Code comes here too,
through tools/ide/pybricksdev.cmd. See that file.

CHANGE (Nov 13): this works on every computer, Windows and Mac. This file,
tools/ide and .vscode/settings.json are on GitHub now, so "git pull" brings
them. On a Mac, the button comes here through tools/ide/pybricksdev.
"""

import datetime
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG_FOLDER = "logs"
LOG_DIR = ROOT / LOG_FOLDER
# Holds pybricksdev.cmd, which sends VS Code's button here.
IDE_DIR = Path(__file__).resolve().parent / "ide"

# Where the logs go on GitHub: the logs folder on this branch.
REMOTE = "origin"
BRANCH = "main"

# Color codes that some tools print. They look like junk in a text file.
COLOR_CODES = re.compile(rb"\x1b\[[0-9;?]*[A-Za-z]")


def open_new_log(program):
    """Make a new log file named after the program and the time right now."""
    LOG_DIR.mkdir(exist_ok=True)
    name = Path(program).stem + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = LOG_DIR / (name + ".log")
    number = 2
    while True:
        try:
            # "x" means: only make a new file, never write over an old one.
            return path, open(path, "x", encoding="utf-8")
        except FileExistsError:
            # Two runs started in the same second. Add a number to the name.
            path = LOG_DIR / (name + "_" + str(number) + ".log")
            number += 1


class Log:
    """Writes lines to the log file with the time in front. Both output
    streams share one Log, so the lock stops two lines from mixing."""

    def __init__(self, file):
        self.file = file
        self.lock = threading.Lock()

    def write(self, text):
        stamp = datetime.datetime.now().strftime("%H:%M:%S")
        with self.lock:
            self.file.write("[" + stamp + "] " + text + "\n")
            # Save right away, so the file is complete even if the computer crashes.
            self.file.flush()

    def write_raw_line(self, raw):
        # A progress bar redraws itself with "\r". Keep only its last drawing.
        raw = raw.rstrip(b"\r").split(b"\r")[-1]
        self.write(COLOR_CODES.sub(b"", raw).decode("utf-8", errors="replace"))


def copy_output(source, terminal, log):
    """Send output to the terminal as soon as it arrives, and each full line to the log."""
    unfinished = b""
    while True:
        chunk = source.read1(4096)
        if not chunk:
            break
        terminal.write(chunk)
        terminal.flush()
        *lines, unfinished = (unfinished + chunk).split(b"\n")
        for line in lines:
            log.write_raw_line(line)
    if unfinished:
        log.write_raw_line(unfinished)


def run_and_log(command, program):
    """Run the command, copy its output to the terminal and a new log file,
    and return its exit code and the log file's path."""
    path, file = open_new_log(program)
    log = Log(file)
    started = datetime.datetime.now()
    log.write("Log started " + started.strftime("%Y-%m-%d %H:%M:%S"))
    log.write("Command: " + subprocess.list2cmdline(command))
    log.write("-" * 40)
    print("Saving output to " + str(path), flush=True)

    # Without these, Python holds the output back until it has a lot of it,
    # and may garble characters that are not plain English letters.
    env = dict(os.environ, PYTHONUNBUFFERED="1", PYTHONIOENCODING="utf-8")
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, env=env)
    copiers = [
        threading.Thread(target=copy_output, args=(process.stdout, sys.stdout.buffer, log)),
        threading.Thread(target=copy_output, args=(process.stderr, sys.stderr.buffer, log)),
    ]
    for copier in copiers:
        copier.start()

    try:
        exit_code = process.wait()
    except KeyboardInterrupt:
        # Ctrl+C reaches pybricksdev too. Wait for it to stop, then close the log.
        log.write("Stopped with Ctrl+C")
        exit_code = process.wait()
    for copier in copiers:
        copier.join()

    ended = datetime.datetime.now()
    log.write("-" * 40)
    log.write("Log ended " + ended.strftime("%Y-%m-%d %H:%M:%S")
              + " after " + str(ended - started).split(".")[0]
              + " (exit code " + str(exit_code) + ")")
    file.close()
    print("Output saved to " + str(path), flush=True)
    return exit_code, path


def git(*args, env=None):
    """Run one git command in the robot folder. Return what it printed, or
    None if it didn't work. Its error messages show in the terminal, so a
    GitHub sign-in window or error can be seen."""
    result = subprocess.run(["git", "-C", str(ROOT), *args], env=env,
                            stdout=subprocess.PIPE, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def failed(reason):
    print("Upload failed: " + reason + " The log files are still saved in the "
          "logs folder, and go up with the next upload that works.", flush=True)
    return False


# CHANGE (Nov 9): before, the log file was committed on this computer and then
# "git push" sent it. That also sent any code commits that were not pushed yet,
# and on another branch the log went to that branch. Now the commit is made
# from what is on GitHub, plus the new log files, and only that is sent.

def upload_logs():
    """Upload every log file that is not on GitHub yet to the logs folder on
    GitHub. Only that folder changes on GitHub, and nothing changes in the
    code on this computer."""
    log_files = sorted(LOG_DIR.glob("*.log"))
    if not log_files:
        return True
    print("Uploading new log files to GitHub (Ctrl+C to skip)", flush=True)
    try:
        return send_new_logs(log_files)
    except FileNotFoundError:
        return failed("git is not installed.")
    except KeyboardInterrupt:
        print("Upload skipped with Ctrl+C. The log files are still saved in the "
              "logs folder, and go up with the next upload.", flush=True)
        return False


def send_new_logs(log_files):
    last_base = None
    # Up to 3 tries, in case a teammate pushes at the same moment.
    for _ in range(3):
        # Get what is on GitHub now. This doesn't change any files here.
        if git("fetch", "--quiet", REMOTE, BRANCH) is None:
            return failed("could not get the latest version from GitHub. Is there internet?")
        base = git("rev-parse", "FETCH_HEAD")
        if base is None:
            return failed("git could not read the latest version from GitHub.")
        if base == last_base:
            # The push didn't work, but nobody else pushed either. Trying again won't help.
            break
        last_base = base

        listing = git("ls-tree", "--name-only", base, LOG_FOLDER + "/")
        if listing is None:
            return failed("git could not list the logs folder on GitHub.")
        on_github = set(listing.splitlines())
        new_files = [f for f in log_files if LOG_FOLDER + "/" + f.name not in on_github]
        if not new_files:
            print("All log files are already on GitHub.", flush=True)
            return True

        # Make a commit that is what's on GitHub plus the new log files. It
        # uses its own index file, so files added with "git add" stay added.
        paths = [LOG_FOLDER + "/" + f.name for f in new_files]
        blobs = git("hash-object", "-w", "--", *paths)
        if blobs is None:
            return failed("git could not read the log files.")
        entries = []
        for blob, path in zip(blobs.splitlines(), paths):
            entries += ["--cacheinfo", "100644," + blob + "," + path]
        with tempfile.TemporaryDirectory() as folder:
            env = dict(os.environ, GIT_INDEX_FILE=os.path.join(folder, "index"))
            tree = None
            if (git("read-tree", base, env=env) is not None
                    and git("update-index", "--add", *entries, env=env) is not None):
                tree = git("write-tree", env=env)
        if not tree:
            return failed("git could not add the log files.")
        if len(new_files) == 1:
            message = "Add run log " + new_files[0].name
        else:
            message = "Add " + str(len(new_files)) + " run logs"
        commit = git("commit-tree", tree, "-p", base, "-m", message)
        if commit is None:
            return failed("git could not make the commit. Are git user.name and user.email set?")

        if git("push", "--quiet", REMOTE, commit + ":refs/heads/" + BRANCH) is not None:
            print("Uploaded to the logs folder on GitHub: "
                  + ", ".join(f.name for f in new_files), flush=True)
            return True
    return failed("git could not push to GitHub.")


def pybricksdev_command():
    """How to start the real pybricksdev, or None if it is not installed."""
    if importlib.util.find_spec("pybricksdev") is not None:
        return [sys.executable, "-m", "pybricksdev"]
    # Not in this Python, so look for pybricksdev.exe. Skip tools/ide, or its
    # pybricksdev.cmd would start this file again.
    folders = []
    for folder in os.environ.get("PATH", "").split(os.pathsep):
        try:
            if folder and Path(folder).resolve() != IDE_DIR:
                folders.append(folder)
        except OSError:
            pass
    found = shutil.which("pybricksdev", path=os.pathsep.join(folders))
    if found:
        return [found]
    # CHANGE (Nov 13): last, look where the "Run on LEGO Brick" button looks
    # first: a .pybricks-venv folder in the home folder.
    venv = Path.home() / ".pybricks-venv"
    for real in (venv / "Scripts" / "pybricksdev.exe", venv / "bin" / "pybricksdev"):
        if real.is_file():
            return [str(real)]
    return None


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python tools/run_logged.py main.py [pybricksdev options]"
              " (python3 on a Mac)")
        return 2
    pybricksdev = pybricksdev_command()
    if pybricksdev is None:
        print("pybricksdev is not installed. Install it with: pip install pybricksdev")
        return 1

    # CHANGE (Nov 9): tools/ide/pybricksdev.cmd hands over the whole command
    # from VS Code, like: run ble --name PixieBricks C:\...\main.py
    # Typed by hand, it is: main.py --name PixieBricks
    if args[:2] == ["run", "ble"]:
        options = args[2:]
    elif args[0].lower().endswith(".py"):
        options = args
    else:
        # Another pybricksdev command, like "pybricksdev devices". No log.
        return subprocess.call(pybricksdev + args)

    spots = [i for i, arg in enumerate(options) if arg.lower().endswith(".py")]
    if not spots:
        return subprocess.call(pybricksdev + ["run", "ble"] + options)
    program = options[spots[-1]]
    others = options[:spots[-1]] + options[spots[-1] + 1:]

    # Only programs in the robot folder get a log. Others run like before.
    if not Path(program).resolve().is_relative_to(ROOT):
        return subprocess.call(pybricksdev + ["run", "ble"] + options)

    command = pybricksdev + ["run", "ble", *others, program]
    exit_code, path = run_and_log(command, program)
    upload_logs()
    return exit_code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)

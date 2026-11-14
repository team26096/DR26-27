@echo off
rem CHANGE (Nov 9): VS CODE'S "RUN ON LEGO BRICK" BUTTON SAVES A LOG AND UPLOADS IT
rem The Pybricks Runner button types this in VS Code's "Pybricks" terminal:
rem     pybricksdev run ble --name "PixieBricks" "C:\Work\darth_rappers_2026\main.py"
rem VS Code's settings put this folder first in the terminal's PATH, so
rem "pybricksdev" starts this file instead of the real one. It hands the whole
rem command to tools\run_logged.py. That runs the real pybricksdev, saves the
rem output in the logs folder, and uploads it to GitHub. Other pybricksdev
rem commands, and programs from outside the robot folder, go to the real
rem pybricksdev with no log.
rem CHANGE (Nov 13): the setting is in .vscode\settings.json in the robot folder,
rem so every computer gets it from GitHub. Where VS Code opens C:\Work instead
rem of the robot folder, it is in C:\Work\.vscode\settings.json. The file
rem "pybricksdev" next to this one does the same on a Mac.
rem If no Python works, the real pybricksdev runs with no log, so the robot
rem still runs.
setlocal
set "python=python"
%python% -c "import sys; sys.exit(sys.version_info < (3, 9))" >nul 2>nul && goto run_logged
set "python=py"
%python% -c "import sys; sys.exit(sys.version_info < (3, 9))" >nul 2>nul && goto run_logged
goto no_python

:run_logged
%python% "%~dp0..\run_logged.py" %*
exit /b %errorlevel%

:no_python
set "real="
for /f "delims=" %%p in ('where pybricksdev.exe 2^>nul') do if not defined real set "real=%%p"
if not defined real (
    echo pybricksdev is not installed. Install it with: pip install pybricksdev
    exit /b 1
)
echo No Python found, so no log is saved this time.
"%real%" %*
exit /b %errorlevel%

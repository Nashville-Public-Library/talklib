:: This will launch the python script.
:: WireReady cannot run .py files, so a batch file is needed to do it.
:: WireReady will run the batch file which runs the python file.

:: turn echo off
@echo off

:: change to current directory (directory of batch file)
CD /d "%~dp0"

:: run python script
py %CD%\SomeFile.py

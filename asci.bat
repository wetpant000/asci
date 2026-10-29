@echo off
where py >NUL 2>NUL
if %errorlevel%==0 (py -3 "%~dp0asci.py" %*) else (python "%~dp0asci.py" %*)

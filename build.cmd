@echo off
REM Requires some kind of bashshell (WSL or cygwin)
set shell="bash"
set python="py"

REM windows build
IF "%1"=="build" (
    %python% setup.py bdist_wininst
)

%shell% build.sh %1
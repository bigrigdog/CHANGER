@echo off

REM Run pylint to check code quality
pylint *.py

REM Run isort to sort imports
isort .

REM Run black to format code
black .

echo Optimization completed.

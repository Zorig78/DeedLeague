@echo off
CALL venv\Scripts\activate
echo Virtual environment loaded
flask run --debug --host=0.0.0.0
pause
cmd /k
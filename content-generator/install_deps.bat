@echo off
echo Installing content-generator dependencies...
python3 -m pip install -r requirements.txt
echo.
echo Dependencies installed successfully!
echo.
echo Now you can run:
echo   python3 generate_algorithms.py --validate
echo   python3 generate_algorithms.py --generate
pause

@echo off
echo Choose a project:
echo 1. Projectile Motion
echo 2. SIR Disease Model
set /p choice=Enter 1 or 2:
if "%choice%"=="1" (
  cd projectile_motion
) else if "%choice%"=="2" (
  cd sir_model
) else (
  echo Invalid choice.
  pause
  exit /b
)
python -m pip install -r requirements.txt
python -m streamlit run app.py
pause

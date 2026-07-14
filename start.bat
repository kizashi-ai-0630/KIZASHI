@echo off
cd /d "%~dp0"
title KIZASHI

if not exist ".venv" (
  echo Setting up KIZASHI. Please wait...
  py -m venv .venv
  call .venv\Scripts\activate.bat
  python -m pip install --upgrade pip
  pip install -r requirements.txt
) else (
  call .venv\Scripts\activate.bat
)

python -m streamlit run app.py
pause

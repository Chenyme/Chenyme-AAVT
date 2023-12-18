@echo off
setlocal
set "script_path=%~dp0"
cd /d "%script_path%"
streamlit run AAMT.py
endlocal
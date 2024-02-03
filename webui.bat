@echo off
setlocal
set "script_path=%~dp0"
cd /d "%script_path%"
streamlit run AAVT.py
endlocal
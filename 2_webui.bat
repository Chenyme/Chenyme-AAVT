@echo off
chcp 65001 > nul
setlocal
set "script_path=%~dp0"
cd /d "%script_path%"

REM 获取字体目录
python utils/font_data.py

REM 启动webui
streamlit run AAVT-HomePage.py

endlocal
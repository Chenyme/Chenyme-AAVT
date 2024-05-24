@echo off
chcp 65001 > nul
setlocal
set "script_path=%~dp0"
cd /d "%script_path%"
powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"

REM 激活环境
call env\Scripts\activate.bat

REM 获取字体目录
python utils/font_data.py

REM 启动webui
streamlit run Chenyme-AAVT.py

endlocal
@echo off
chcp 65001 > nul
setlocal

REM 设置脚本路径
set "script_path=%~dp0"
cd /d "%script_path%"

REM 检查 PowerShell 是否可用
where powershell > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] PowerShell not found. Please ensure PowerShell is installed.
    exit /b 1
)

REM 设置 PowerShell 执行策略
echo Setting PowerShell execution policy...
powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to set PowerShell execution policy.
    exit /b 1
)

REM 激活虚拟环境
echo Activating virtual environment...
if exist env\Scripts\activate.bat (
    call env\Scripts\activate.bat
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to activate the virtual environment.
        exit /b 1
    )
) else (
    echo [ERROR] Virtual environment not found. Please ensure it is created.
    exit /b 1
)

REM 确保返回到脚本目录
cd /d "%script_path%"

REM 提示用户关于 Streamlit 的电子邮件提示
echo Launching Streamlit Web UI...
echo NOTE: 若有 Streamlit 的电子邮件提示直接Enter 跳过

python styles\info.py

REM 启动 Streamlit Web UI
streamlit run Chenyme-AAVT.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] 运行出错！
    echo.
    echo "若显示 OMP: Error #15，请点击项目目录中的闪退修复！"
    echo "若显示其他报错，请前往GitHub或群内反馈！"
    echo.
    pause
)

REM 清理环境
endlocal
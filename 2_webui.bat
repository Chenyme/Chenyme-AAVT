@echo off
chcp 65001 > nul
setlocal

REM 设置脚本路径
set "script_path=%~dp0"
cd /d "%script_path%"

REM 检查 PowerShell 是否可用
where powershell > nul 2>&1
if %errorlevel% neq 0 (
    echo [❌ ERROR] PowerShell not found. Please ensure PowerShell is installed.
    exit /b 1
)

REM 设置 PowerShell 执行策略
echo Setting PowerShell execution policy...
powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"
if %errorlevel% neq 0 (
    echo [❌ ERROR] Failed to set PowerShell execution policy.
    exit /b 1
)

REM 激活虚拟环境
echo Activating virtual environment...
if exist env\Scripts\activate.bat (
    call env\Scripts\activate.bat
    if %errorlevel% neq 0 (
        echo [❌ ERROR] Failed to activate the virtual environment.
        exit /b 1
    )
) else (
    echo [❌ ERROR] Virtual environment not found. Please ensure it is created.
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
    echo [❌ ERROR] 运行出错！
    echo.
    echo "若显示 缺失 fbgemm.dll，请使用Install选择修复版本！"
    echo "若显示 缺失 cudnn_ops_infer64_8.dll 请前往GitHub下载相关dll！"
    echo "若有其他报错，请阅读常见问题，或前往GitHub 或 群组讨论！"
    echo.
    pause
)

REM 清理环境
endlocal
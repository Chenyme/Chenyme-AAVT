@echo off
chcp 65001 > nul
setlocal

echo ====================================================
echo            系统环境检测脚本
echo ====================================================
echo.
echo 检测系统环境中是否安装 CUDA、FFmpeg 和 Python...
echo.

REM 假设是在 Windows 上运行，通过 where 检测
set "CHECK_CMD=where"

REM 检测 Python
echo [检测] 正在检测 Python...
%CHECK_CMD% python >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请确认已正确安装。
) else (
    echo [成功] Python 已安装。
)
echo.

REM 检测 FFmpeg
echo [检测] 正在检测 FFmpeg...
%CHECK_CMD% ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 FFmpeg，请确认已正确安装。
) else (
    echo [成功] FFmpeg 已安装。
)
echo.

REM 检测 CUDA
echo [检测] 正在检测 CUDA...
%CHECK_CMD% nvcc >nul 2>&1
if %errorlevel% neq 0 (
    echo [失败] 未检测到 CUDA，若为CPU用户可忽略！
) else (
    echo [成功] CUDA 已安装。
)
echo.

echo ====================================================
echo         环境检测完成！可以正常执行安装脚本！
echo ====================================================
echo.

echo 按 Enter 键退出...
pause


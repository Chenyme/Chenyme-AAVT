@echo off
chcp 65001 > nul
setlocal

set "script_path=%~dp0"
cd /d "%script_path%"
powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"


REM 检查虚拟环境是否存在
if not exist env (
    echo 创建新项目环境...
    python -m venv env
) else (
    echo 虚拟环境已存在，跳过创建步骤
)

REM 激活新项目环境
call env\Scripts\activate.bat

REM 设置pip镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

REM 检查和更新 anthropic
pip show anthropic > nul
if %errorlevel% equ 0 (
    echo 更新 anthropic...
    pip install --upgrade anthropic
) else (
    echo 安装 anthropic...
    pip install anthropic
)

REM 检查和更新 google-generativeai
pip show google-generativeai > nul
if %errorlevel% equ 0 (
    echo 更新 google-generativeai...
    pip install --upgrade google-generativeai
) else (
    echo 安装 google-generativeai...
    pip install google-generativeai
)

echo 更新完成
pause
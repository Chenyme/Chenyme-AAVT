@echo off
chcp 65001 > nul
setlocal


REM 用户确认
:prompt
set /p userInput="请确认您已安装好CUDA12.1，输入 'yes' 继续，其他输入将自动停止安装脚本: "


if /i "%userInput%"=="yes" (
    echo 您输入了yes，继续执行脚本。
) else (
    echo 程序将停止
    exit /b
)


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


echo 正在检查和更新库...


REM 设置pip镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple


pip install --upgrade pip

pip uninstall streamlit

REM 检查和更新 streamlit
pip show streamlit > nul
if %errorlevel% equ 0 (
    echo 更新 streamlit...
    pip install streamlit==1.37.0
) else (
    echo 安装 streamlit...
    pip install streamlit==1.37.0
)


REM 检查和更新 streamlit-antd-components
pip show streamlit-antd-components > nul
if %errorlevel% equ 0 (
    echo 更新 streamlit-antd-components...
    pip install --upgrade streamlit-antd-components
) else (
    echo 安装 streamlit-antd-components...
    pip install streamlit-antd-components
)


REM 检查和更新 openai
pip show openai > nul
if %errorlevel% equ 0 (
    echo 更新 openai...
    pip install --upgrade openai
) else (
    echo 安装 openai...
    pip install openai
)

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

REM 检查并卸载 torch torchvision torchaudio
echo 检查 torch torchvision torchaudio
pip show torch > nul
if %errorlevel% equ 0 (
    echo 卸载 torch torchvision torchaudio...
    pip uninstall -y torch torchvision torchaudio
)


echo 安装 torch torchvision torchaudio...
echo 国内环境不稳定，建议开启VPN下载
pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu121


REM 检查和更新 faster-whisper
pip show faster-whisper > nul
if %errorlevel% equ 0 (
    echo 更新 faster-whisper...
    pip install --upgrade faster-whisper
) else (
    echo 安装 faster-whisper...
    pip install faster-whisper
)


REM 检查和更新 opencv-python
pip show opencv-python > nul
if %errorlevel% equ 0 (
    echo 更新 opencv-python...
    pip install --upgrade opencv-python
) else (
    echo 安装 opencv-python...
    pip install opencv-python
)


echo 更新完成
pause
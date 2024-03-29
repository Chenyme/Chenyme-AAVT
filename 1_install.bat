@echo off
chcp 65001 > nul
setlocal
set "script_path=%~dp0"
cd /d "%script_path%"
powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"

REM 创建新项目环境
python -m venv env

REM 激活新项目环境
call env\Scripts\activate.bat

echo 正在检查和更新库...

REM 设置pip镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

pip install --upgrade pip

REM 检查和更新 streamlit
pip show streamlit > nul
if %errorlevel% equ 0 (
    echo 更新 streamlit...
    pip install --upgrade streamlit
) else (
    echo 安装 streamlit...
    pip install streamlit
)

REM 检查和更新 openai-whisper
pip show openai-whisper > nul
if %errorlevel% equ 0 (
    echo 更新 openai-whisper...
    pip install --upgrade openai-whisper
) else (
    echo 安装 openai-whisper...
    pip install openai-whisper
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

REM 检查和更新 langchain
pip show langchain > nul
if %errorlevel% equ 0 (
    echo 更新 langchain...
    pip install --upgrade langchain
) else (
    echo 安装 langchain...
    pip install langchain
)

REM 检查和更新 torch torchvision torchaudio
pip show torch torchvision torchaudio > nul
if %errorlevel% equ 0 (
    echo 更新 torch torchvision torchaudio...
    pip install --upgrade torch torchvision torchaudio
) else (
    echo 安装 torch torchvision torchaudio...
    pip install torch torchvision torchaudio
)

REM 检查和更新 faster-whisper
pip show faster-whisper > nul
if %errorlevel% equ 0 (
    echo 更新 faster-whisper...
    pip install --upgrade faster-whisper
) else (
    echo 安装 faster-whisper...
    pip install faster-whisper
)

REM 检查和更新 langchain-openai
pip show langchain-openai > nul
if %errorlevel% equ 0 (
    echo 更新 langchain-openai...
    pip install --upgrade langchain-openai
) else (
    echo 安装 langchain-openai...
    pip install langchain-openai
)

echo 更新完成
pause
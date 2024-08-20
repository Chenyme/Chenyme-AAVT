@echo off
chcp 65001 > nul
setlocal

REM 创建新项目环境
echo.
echo 正在创建新的虚拟环境...
python -m venv env

if exist env\Scripts\activate.bat (
    REM 激活新项目环境
    echo 虚拟环境已成功创建和激活！
    call env\Scripts\activate.bat
    echo.
) else (
    echo [错误] 虚拟环境创建失败。
    exit /b 1
)

REM 检查 torch、torchvision、torchaudio 是否已安装
pip show torch torchvision torchaudio >nul 2>&1

REM 如果没有安装则退出
if %errorlevel% neq 0 (
    echo [信息] 未检测到 torch、torchvision、torchaudio，无需删除。
    exit /b 0
)

REM 如果安装了则提示用户是否确认删除
set /p confirm="检测到已安装的 torch、torchvision、torchaudio。你确定要删除它们吗？ (Y/N): "

REM 判断用户输入，不区分大小写
if /i "%confirm%" neq "Y" (
    goto skip_uninstall
)

REM 执行删除操作
pip uninstall -y torch torchvision torchaudio
if %errorlevel% neq 0 (
    echo [错误] 删除现有的 torch, torchvision, torchaudio 失败。
    exit /b 1
)
echo [成功] torch, torchvision, torchaudio 已成功删除。

:skip_uninstall
echo [跳过操作] 用户选择不删除，继续执行剩余脚本。
echo.

:choose_cuda_version
echo ================================================
echo                CUDA 版本选择菜单
echo ================================================
echo 1. CUDA 11.8
echo 2. CUDA 12.1
echo 3. CUDA 12.4
echo 4. CPU版本（无CUDA支持）
echo ================================================
echo.

set /p cuda_choice="请输入选项(1-4): "

REM 验证输入是否为合法选项
if "%cuda_choice%"=="1" (
    set "cuda_version=11.8"
    echo 您选择了 CUDA 11.8 版本，相关软件包将根据此版本安装，并将执行降级操作。
    goto cuda11_8_install
) else if "%cuda_choice%"=="2" (
    set "cuda_version=12.1"
    echo 您选择了 CUDA 12.1 版本，相关软件包将根据此版本安装。
    goto cuda12_1_install
) else if "%cuda_choice%"=="3" (
    set "cuda_version=12.4"
    echo 您选择了 CUDA 12.4 版本，相关软件包将根据此版本安装。
    goto cuda12_4_install
) else if "%cuda_choice%"=="4" (
    set "cuda_version=CPU"
    echo 您选择了 CPU 版本，将不安装 CUDA 相关软件包。
    goto cpu_install
) else (
    echo.
    echo 输入无效，请输入 1 到 4 之间的数字！
    echo.
    goto choose_cuda_version
)

:cuda11_8_install
echo.
echo 正在安装 CUDA 11.8 版本相关软件包...
echo 国内环境不稳定，建议开启 VPN 下载
echo.

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
if %errorlevel% neq 0 (
    echo [错误] 安装 torch, torchvision, torchaudio 失败，请检查网络或 VPN。
    exit /b 1
)

echo.
echo 最新版本 ctranslate2 仅支持 CUDA 12，正在降级到适用于 CUDA 11.8 的版本...
pip install --force-reinstall ctranslate2==3.24.0
if %errorlevel% neq 0 (
    echo [错误] 安装 ctranslate2 版本 3.24.0 失败。
    exit /b 1
)

goto common_install

:cuda12_1_install
echo.
echo 正在安装 CUDA 12.1 版本相关软件包...
echo 国内环境不稳定，建议开启 VPN 下载
echo.

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
if %errorlevel% neq 0 (
    echo [错误] 安装 torch, torchvision, torchaudio 失败，请检查网络或 VPN。
    exit /b 1
)

goto common_install

:cuda12_4_install
echo.
echo 正在安装 CUDA 12.4 版本相关软件包...
echo 国内环境不稳定，建议开启 VPN 下载
echo.

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
if %errorlevel% neq 0 (
    echo [错误] 安装 torch, torchvision, torchaudio 失败，请检查网络或 VPN。
    exit /b 1
)

goto common_install

:cpu_install
echo.
echo 正在安装 CPU 版本相关软件包...
echo.

pip install torch torchvision torchaudio
if %errorlevel% neq 0 (
    echo [错误] 安装 torch, torchvision, torchaudio 失败，请检查网络或 VPN。
    exit /b 1
)

goto common_install

:common_install
echo.
echo          正在安装其他通用库...
echo.

pip install streamlit==1.37.1
pip install streamlit-antd-components==0.3.2
pip install openai==1.41.0
pip install anthropic==0.34.0
pip install google-generativeai==0.7.2
pip install faster-whisper==1.0.3
pip install opencv-python==4.10.0.84
pip install pandas==2.2.2
pip uninstall -y numpy
pip install numpy

if %errorlevel% neq 0 (
    echo [错误] 安装部分库失败，请检查网络或其他问题。
    exit /b 1
)

echo.
echo 所有软件包已成功安装！
echo 按任意键退出！
echo.

pause

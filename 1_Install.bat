@echo off
chcp 65001 > nul
setlocal

:: 初始化检测标志
set "ENV_CHECK_SUCCESS=1"

echo === 依赖环境检测 ===
echo.

:: 检测 Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 未检测到 Python，请确认已正确安装。
    set "ENV_CHECK_SUCCESS=0"
) else (
    echo [✔️ OK] Python 已安装
)

:: 检测 FFmpeg
where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 未检测到 FFmpeg，请确认已正确安装。
    set "ENV_CHECK_SUCCESS=0"
) else (
    echo [✔️ OK] FFMpeg 已安装
)

:: 检查是否通过所有检测
if "%ENV_CHECK_SUCCESS%"=="0" (
    echo [❌ ERROR] 检测未通过！
    echo.
    echo 安装已退出，请安装上述缺失的环境后重试！
    echo.
    pause >nul
    exit /b 1
)

echo [✔️ OK] Env 检测已通过

echo.
echo.

:: 创建虚拟环境
echo === 创建虚拟环境 ===
echo.
python -m venv env

if exist env\Scripts\activate.bat (
    echo [✔️ OK] 虚拟环境创建成功
    call env\Scripts\activate.bat
    echo [✔️ OK] 虚拟环境成功激活
) else (
    echo [❌ ERROR] 虚拟环境创建失败
    exit /b 1
)


:: 检查 torch、torchvision、torchaudio 是否安装
pip show torch torchvision torchaudio >nul 2>&1
if %errorlevel% neq 0 (
    echo [❔ INFO] 未检测到 torch、torchvision、torchaudio，跳过此步骤
) else (
    echo.

    set /p confirm="检测到 torch、torchvision、torchaudio 已安装，是否卸载重装（版本修复也请按 Y）？ (Y/N): "

    if /i "%confirm%"=="Y" (
        pip uninstall -y torch torchvision torchaudio
        if %errorlevel% neq 0 (
            echo [❌ ERROR] 删除 torch、torchvision、torchaudio 失败。
            exit /b 1
        )
        echo [✔️ OK] 已成功删除 torch、torchvision、torchaudio。
    ) else (
        echo.
        echo [✔️ OK] 已跳过 Pytorch 卸载安装步骤

        goto continue_install_common
    )
)


echo.

:: Pytorch 版本选择
echo === 自定义 Pytorch 参数 ===

:choose_torch_version
echo.
echo Pytorch 版本

echo 1. 最新版本 (2.4.0)
echo 2. 修复版本 (2.4.1)
echo.

echo 若您运行遇到 OSError: [WinError 126] Not found fbgemm.dll时 请选择修复版本

set /p torch_version_choice="请输入选项(1-2): "

if "%torch_version_choice%"=="1" (
    set "torch_version=2.4.0"
    goto choose_cuda_version
) else if "%torch_version_choice%"=="2" (
    set "torch_version=2.4.1"
    goto choose_cuda_version
) else (
    echo [❌ ERROR] 输入无效，请输入 1 到 2 之间的数字。
    goto choose_torch_version
)



:choose_cuda_version
echo.
echo CUDA 版本

echo 1. CUDA 11.8
echo 2. CUDA 12.1
echo 3. CUDA 12.4
echo 4. CPU（不使用 CUDA）
echo.

set /p cuda_choice="请输入选项(1-4): "

if "%cuda_choice%"=="1" (
    set "cuda_version=118"
    goto continue_install
) else if "%cuda_choice%"=="2" (
    set "cuda_version=121"
    goto continue_install
) else if "%cuda_choice%"=="3" (
    set "cuda_version=124"
    goto continue_install
) else if "%cuda_choice%"=="4" (
    set "cuda_version=CPU"
    goto continue_install
) else (
    echo [❌ ERROR] 输入无效，请输入 1 到 4 之间的数字。
    goto choose_cuda_version
)

:continue_install

echo.

:: 安装相应的 CUDA 或 CPU 版本软件包
if "%cuda_version%"=="CPU" (

    echo [✔️ OK] 正在进行安装 CPU 版本
    echo.

    if "%torch_version%"=="2.4.0" (
        pip install torch torchvision torchaudio
    ) else (
        pip install torch==2.4.1 torchvision torchaudio
    )

) else (
    echo [✔️ OK] 正在进行安装 CUDA %cuda_version% 版本
    if "%torch_version%"=="2.4.0" (
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu%cuda_version%
    ) else (
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/test/cu124
    )
)

echo.

:: 通用库安装

:continue_install_common
echo.
echo.
echo === 安装依赖库 ===
echo.
echo [✔️ OK] 正在进行安装其他通用依赖库
echo.

pip install streamlit==1.37.1 streamlit-antd-components==0.3.2
pip install openai anthropic google-generativeai faster-whisper opencv-python pandas
pip uninstall -y numpy
pip install "numpy<2.0.0"

if %errorlevel% neq 0 (

    echo [❌ ERROR] 库安装失败。

    exit /b 1
    pause >nul
)

echo.
echo.
echo [✔️ OK] 成功安装，脚本执行完成！

pause >nul
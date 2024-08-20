@echo off
chcp 65001 > nul
setlocal

REM 提示用户确认是否遇到 OMP Error #15
echo.
echo "请确认您是否遇到了 OMP Error #15 的报错问题。"
echo "只有在遇到此错误时才应该运行此脚本进行修复操作。"
echo.
set /p user_input="如果您确认遇到该错误，请输入大写 'Y' 并按回车继续："

REM 确保输入后再检查条件
echo.
if /i "%user_input%"=="Y" (
    echo 您已确认错误，继续执行脚本。
    echo.
) else (
    echo 未确认错误，脚本将退出。
    echo.
    pause
    exit /b
)

set "script_path=%~dp0"

REM 检查文件是否存在并尝试删除
echo 正在检查文件是否存在...
echo.
if exist "%script_path%env\Library\bin\libiomp5md.dll" (
    echo 正在尝试删除文件...
    del "%script_path%env\Library\bin\libiomp5md.dll" >nul 2>&1
    
    REM 检查删除是否成功
    if exist "%script_path%env\Library\bin\libiomp5md.dll" (
        echo 文件删除失败，可能正在被占用！
    ) else (
        echo 文件已成功删除
    )
) else (
    echo 文件不存在，修复退出，请寻找其他libiomp5md.dll文件
)

echo.
pause
endlocal



@echo off
chcp 65001 > nul
setlocal

set "script_path=%~dp0"

if exist "%script_path%env\Library\bin\libiomp5md.dll" (
    del "%script_path%env\Library\bin\libiomp5md.dll"
    if not exist "%script_path%env\Library\bin\libiomp5md.dll" (
        echo 文件已成功删除
    ) else (
        echo 文件删除失败
    )
) else (
    echo 文件不存在
)

pause
endlocal

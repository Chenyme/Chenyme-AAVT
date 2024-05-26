@echo off
chcp 65001 > nul
setlocal


set "script_path=%~dp0"
del "%script_path%env\Library\bin\libiomp5md.dll"
echo 已完成

pause
endlocal


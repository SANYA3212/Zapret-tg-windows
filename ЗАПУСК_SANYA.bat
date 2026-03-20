@echo off
chcp 65001 >nul
title TG_WINDOWS_Proxy_by_SANYA

echo ╔════════════════════════════════════════════════════════╗
echo ║     TG_WINDOWS_Proxy_by_SANYA - Modern Proxy           ║
echo ╚════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ОШИБКА] Python не найден!
    pause
    exit /b 1
)

python -c "import toga" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Установка зависимостей...
    pip install toga-winforms cryptography
)

echo [OK] Запуск TG_WINDOWS_Proxy_by_SANYA...
echo.

set PYTHONPATH=%~dp0src;%PYTHONPATH%
cd "%~dp0src"
python -m tg_sanya_proxy

if %errorlevel% neq 0 (
    echo.
    echo [ОШИБКА] Не удалось запустить приложение
    pause
)

@echo off
chcp 65001 >nul
title TG_WINDOWS_Proxy_by_SANYA - Build EXE

echo ╔════════════════════════════════════════════════════════╗
echo ║     TG_WINDOWS_Proxy_by_SANYA - Сборка EXE             ║
echo ╚════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM Проверка Python
echo [1/4] Проверка Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ОШИБКА: Python не найден!
    pause
    exit /b 1
)
python --version
echo.

REM Установка зависимостей
echo [2/4] Установка зависимостей...
pip install pyinstaller toga-winforms cryptography --quiet
echo.

REM Очистка старых сборок
echo [3/4] Очистка старых сборок...
rmdir /S /Q build dist 2>nul
del /Q *.spec 2>nul
echo.

REM Сборка EXE
echo [4/4] Сборка EXE файла...
echo.

pyinstaller --noconfirm ^
    --windowed ^
    --name "TG_WINDOWS_Proxy_by_SANYA" ^
    --icon=NONE ^
    --add-data "src/tg_sanya_proxy;tg_sanya_proxy" ^
    --hidden-import=toga ^
    --hidden-import=toga.windows ^
    --hidden-import=cryptography ^
    --collect-all toga ^
    --collect-all cryptography ^
    src/tg_sanya_proxy/__main__.py

if %errorlevel% neq 0 (
    echo.
    echo ════════════════════════════════════════════════════════
    echo ОШИБКА СБОРКИ!
    echo ════════════════════════════════════════════════════════
    pause
    exit /b 1
)

REM Копирование в release
echo.
echo ════════════════════════════════════════════════════════
echo Копирование в папку release...
echo ════════════════════════════════════════════════════════

rmdir /S /Q release 2>nul
mkdir release

xcopy /E /I /Y dist\TG_WINDOWS_Proxy_by_SANYA release\TG_WINDOWS_Proxy_by_SANYA
xcopy /Y README.md release\
xcopy /Y LICENSE release\

echo.
echo ════════════════════════════════════════════════════════
echo СБОРКА ЗАВЕРШЕНА!
echo ════════════════════════════════════════════════════════
echo.
echo EXE файл находится в папке: release\TG_WINDOWS_Proxy_by_SANYA\
echo.
echo Для запуска выполните:
echo   release\TG_WINDOWS_Proxy_by_SANYA\TG_WINDOWS_Proxy_by_SANYA.exe
echo.

pause

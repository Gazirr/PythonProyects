@echo off
cd /d "%~dp0"
echo Ejecutando aplicacion desde: %CD%
set PYTHONPATH=%PYTHONPATH%;%CD%
.\venv_new\Scripts\python.exe -m src.main_app
if %ERRORLEVEL% neq 0 (
    echo.
    echo Error al ejecutar la aplicacion. 
    echo Verifique que las dependencias esten correctamente instaladas en venv_new.
)
pause

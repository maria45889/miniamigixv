@echo off
title MiniAmigixV - Servidor
echo.
echo  ========================================
echo    🐾 MiniAmigixV - Iniciando servidor
echo  ========================================
echo.

:: Activar entorno virtual y levantar servidor
cd /d "%~dp0"

:: Abrir navegador automaticamente despues de 2 segundos
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:8000"

:: Iniciar Django
echo  ✅ Servidor corriendo en http://127.0.0.1:8000
echo  ❌ Para detener: Ctrl+C
echo.
call venv\Scripts\python.exe manage.py runserver
pause

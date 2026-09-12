@echo off
setlocal enabledelayedexpansion
title Steve Minecraft PNG - Local Server
echo.
echo  ===============================================
echo   Steve Minecraft PNG - local server
echo  ===============================================
echo.
cd /d "%~dp0"
python --version >nul 2>&1
if %errorlevel% neq 0 (
  py --version >nul 2>&1
  if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Install from python.org
    pause
    exit /b 1
  ) else (
    set PY=py
  )
) else (
  set PY=python
)
netstat -ano | findstr :8000 >nul
if %errorlevel% equ 0 (
  echo [INFO] Port 8000 already in use - opening site...
  goto OPEN
)
echo [1/3] Starting server at http://localhost:8000 ...
start "Steve Server 8000" %PY% -m http.server 8000
echo [2/3] Waiting for server...
for /L %%i in (1,1,10) do (
  powershell -Command "try{Invoke-WebRequest -Uri http://localhost:8000/3d.html -UseBasicParsing -TimeoutSec 1 | Out-Null; exit 0}catch{exit 1}"
  if !errorlevel! equ 0 goto OPEN
  timeout /t 1 /nobreak >nul
)
:OPEN
echo [3/3] Opening site in browser...
start http://localhost:8000/3d.html
echo.
echo  ===============================================
echo   DONE!
echo   3D main   : http://localhost:8000/3d.html
echo   Offline   : http://localhost:8000/3d-offline.html
echo  ===============================================
echo.
echo   To stop - close window "Steve Server 8000" or press Ctrl+C
echo.
pause

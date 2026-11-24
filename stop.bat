@echo off
title IntelliFlow - Stop Services
echo ===================================================================
echo   IntelliFlow: Terminating All Running Services and Simulations...
echo ===================================================================

echo [1/3] Terminating SUMO simulation processes (sumo.exe, sumo-gui.exe)...
taskkill /F /IM sumo.exe >nul 2>&1
taskkill /F /IM sumo-gui.exe >nul 2>&1

echo [2/3] Terminating IntelliFlow Web UI (Vite / Node server)...
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { ($_.Name -eq 'node.exe') -and ($_.CommandLine -like '*vite*' -or $_.CommandLine -like '*IntelliFlow*frontend*' -or $_.CommandLine -like '*project*frontend*') } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }" >nul 2>&1

echo [3/3] Terminating any active Python simulation runners...
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { ($_.Name -eq 'python.exe') -and ($_.CommandLine -like '*IntelliFlow*' -or $_.CommandLine -like '*final year*project*') } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }" >nul 2>&1

echo.
echo [SUCCESS] All IntelliFlow instances, SUMO simulations, and Web UI servers stopped cleanly.
echo ===================================================================

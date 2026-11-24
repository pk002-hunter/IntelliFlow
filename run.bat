@echo off
title IntelliFlow - AI Adaptive Traffic Signal Control
cd /d "%~dp0"

set PYTHON=%~dp0venv\Scripts\python.exe
if not exist "%PYTHON%" set PYTHON=python

set STREAMLIT=%~dp0venv\Scripts\streamlit.exe
if not exist "%STREAMLIT%" set STREAMLIT=streamlit

set SUMO_BIN=C:\Program Files (x86)\Eclipse\Sumo\bin\sumo-gui.exe
if not exist "%SUMO_BIN%" set SUMO_BIN=sumo-gui

if "%1"=="dashboard" goto :run_dashboard
if "%1"=="demo_mukhani" goto :run_demo_mukhani
if "%1"=="demo_haldwani" goto :run_demo_haldwani
if "%1"=="real" goto :run_gui_real
if "%1"=="morning" goto :run_gui_morning
if "%1"=="evening" goto :run_gui_evening
if "%1"=="yolo" goto :run_yolo
if "%1"=="eval" goto :run_eval
if "%1"=="test" goto :run_test

:menu
cls
echo ===================================================================
echo   IntelliFlow: AI Adaptive Traffic Signal Control (Team #54)
echo   Case Study: Mukhani Chauraha and Full Haldwani Road Network
echo ===================================================================
echo   [AI-CONTROLLED LIVE DEMOS - PPO REINFORCEMENT LEARNING]
echo   1. Mukhani Chauraha 10-Lane Junction (Live AI Signal Control)
echo   2. Full Haldwani City Corridors (Live AI Signal Control)
echo.
echo   [STANDALONE ROAD NETWORK AND PEAK TRAFFIC VISUALIZERS]
echo   3. View Complete 37,000+ Streets Real OSM City Network
echo      - Matches Google Maps: Kathgodam down to Motahaldu
echo   4. View Morning Peak Hour Traffic Rush (8:00 AM - 10:30 AM)
echo   5. View Evening Peak Hour Traffic Rush (5:30 PM - 8:30 PM)
echo.
echo   [COMPUTER VISION, DASHBOARD AND VALIDATION]
echo   6. Run YOLOv8 Computer Vision Bridge (Traffic State Estimation)
echo   7. Launch Interactive Web Dashboard (Streamlit App)
echo   8. Run Empirical Benchmark and Statistical Hypothesis Tests
echo   9. Run Project Test Suite (pytest - 4/4 Tests)
echo   0. Exit
echo ===================================================================
set /p choice="Select an option [1-9, or 0]: "

if "%choice%"=="1" goto :run_demo_mukhani
if "%choice%"=="2" goto :run_demo_haldwani
if "%choice%"=="3" goto :run_gui_real
if "%choice%"=="4" goto :run_gui_morning
if "%choice%"=="5" goto :run_gui_evening
if "%choice%"=="6" goto :run_yolo
if "%choice%"=="7" goto :run_dashboard
if "%choice%"=="8" goto :run_eval
if "%choice%"=="9" goto :run_test
if "%choice%"=="0" exit /b 0
goto :menu

:run_demo_mukhani
echo.
echo ===================================================================
echo   Launching Live AI Demo with PPO Agent: Mukhani Chauraha
echo   (AI model actively optimizes green phases via TraCI)
echo ===================================================================
"%PYTHON%" scripts\demo.py --network mukhani --agent ppo --delay 45
pause
goto :menu

:run_demo_haldwani
echo.
echo ===================================================================
echo   Launching Live AI Demo with PPO Agent: Full Haldwani Network
echo   (AI model actively manages arterials and hospital corridors)
echo ===================================================================
"%PYTHON%" scripts\demo.py --network haldwani --agent ppo --delay 35
pause
goto :menu

:run_gui_real
echo.
echo ===================================================================
echo   Opening SUMO-GUI: 37,000+ Streets Real OSM City Road Network
echo   Matching Google Maps: Kathgodam down to Motahaldu
echo ===================================================================
start "" "%SUMO_BIN%" -c "%~dp0sumo\networks\haldwani_full\haldwani_real.sumocfg"
goto :menu

:run_gui_morning
echo.
echo ===================================================================
echo   Opening SUMO-GUI: Morning Peak Hour (8:00 AM - 10:30 AM)
echo   Heavy Inbound Surge: Kathgodam and Kaladhungi to Center
echo ===================================================================
start "" "%SUMO_BIN%" -c "%~dp0sumo\networks\mukhani_chauraha\mukhani_morning.sumocfg"
goto :menu

:run_gui_evening
echo.
echo ===================================================================
echo   Opening SUMO-GUI: Evening Peak Hour (5:30 PM - 8:30 PM)
echo   Heavy Outbound Surge: Center to Kathgodam and Kaladhungi
echo ===================================================================
start "" "%SUMO_BIN%" -c "%~dp0sumo\networks\mukhani_chauraha\mukhani_evening.sumocfg"
goto :menu

:run_yolo
echo.
echo ===================================================================
echo   Running YOLOv8 Computer Vision Perception and State Estimation
echo ===================================================================
"%PYTHON%" scripts\yolo_traffic_detector.py morning
pause
goto :menu

:run_dashboard
echo.
echo ===================================================================
echo   Starting IntelliFlow Web Dashboard...
echo   Open your browser at: http://localhost:8501
echo ===================================================================
"%STREAMLIT%" run src\dashboard\app.py
pause
goto :menu

:run_eval
echo.
echo ===================================================================
echo   Running Empirical Benchmark: Fixed vs Actuated vs DQN vs PPO
echo ===================================================================
"%PYTHON%" scripts\evaluate.py --network mukhani --episodes 10 --gui
pause
goto :menu

:run_test
echo.
echo ===================================================================
echo   Running Pytest Test Suite across all environments
echo ===================================================================
"%PYTHON%" -m pytest tests/ -v
pause
goto :menu

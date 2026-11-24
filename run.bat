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
if "%1"=="demo_fixed" goto :run_demo_fixed
if "%1"=="demo_actuated" goto :run_demo_actuated
if "%1"=="demo_dqn" goto :run_demo_dqn
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
echo   [LIVE SUMO-GUI SIMULATIONS: AI vs CLASSICAL BASELINES]
echo   1. Mukhani Chauraha - Trained PPO AI Control (Live SUMO-GUI)
echo   2. Mukhani Chauraha - Webster's Fixed-Time Cycles (Baseline 1)
echo   3. Mukhani Chauraha - Inductive Loop Sensor-Actuated (Baseline 2)
echo   4. Mukhani Chauraha - Double DQN Agent (Baseline 3)
echo   5. Full Haldwani City Corridors (Live AI Signal Control)
echo.
echo   [STANDALONE ROAD NETWORK AND PEAK TRAFFIC VISUALIZERS]
echo   6. View Complete 37,000+ Streets Real OSM City Network
echo      - Matches Google Maps: Kathgodam down to Motahaldu
echo   7. View Morning Peak Hour Traffic Rush (8:00 AM - 10:30 AM)
echo   8. View Evening Peak Hour Traffic Rush (5:30 PM - 8:30 PM)
echo.
echo   [COMPUTER VISION, DASHBOARD AND EMPIRICAL BENCHMARK]
echo   9. Run YOLOv8 Computer Vision Bridge (Traffic State Estimation)
echo   10. Launch Interactive Web Dashboard (Streamlit App - Full Metrics)
echo   11. Run Empirical Benchmark and Statistical Tests (Summary + Plots)
echo   12. Run Project Test Suite (pytest - 4/4 Tests)
echo   0. Exit
echo ===================================================================
set /p choice="Select an option [1-12, or 0]: "

if "%choice%"=="1" goto :run_demo_mukhani
if "%choice%"=="2" goto :run_demo_fixed
if "%choice%"=="3" goto :run_demo_actuated
if "%choice%"=="4" goto :run_demo_dqn
if "%choice%"=="5" goto :run_demo_haldwani
if "%choice%"=="6" goto :run_gui_real
if "%choice%"=="7" goto :run_gui_morning
if "%choice%"=="8" goto :run_gui_evening
if "%choice%"=="9" goto :run_yolo
if "%choice%"=="10" goto :run_dashboard
if "%choice%"=="11" goto :run_eval
if "%choice%"=="12" goto :run_test
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

:run_demo_fixed
echo.
echo ===================================================================
echo   Launching Webster's Fixed-Time Simulation: Mukhani Chauraha
echo   (Fixed splits: 45s EW Kaladhungi Rd, 30s NS Canal Rd, 3s Yellow)
echo ===================================================================
"%PYTHON%" scripts\demo.py --network mukhani --agent fixed --delay 45
pause
goto :menu

:run_demo_actuated
echo.
echo ===================================================================
echo   Launching Sensor-Actuated Simulation: Mukhani Chauraha
echo   (Inductive Loop Gap-Out: Min Green 10s, Max Green 50s)
echo ===================================================================
"%PYTHON%" scripts\demo.py --network mukhani --agent actuated --delay 45
pause
goto :menu

:run_demo_dqn
echo.
echo ===================================================================
echo   Launching Live AI Demo with Double DQN: Mukhani Chauraha
echo ===================================================================
"%PYTHON%" scripts\demo.py --network mukhani --agent dqn --delay 45
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
"%PYTHON%" scripts\evaluate.py
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

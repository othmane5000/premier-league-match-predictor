@echo off
title Construction de l'application .exe
color 0B
cd /d "%~dp0\.."

echo ============================================
echo   CONSTRUCTION DE L'APPLICATION DESKTOP
echo   Football Match Predictor
echo ============================================
echo.

echo [1/4] Installation des dependances de build...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt
python -m pip install --quiet pyinstaller pywebview

echo [2/4] Nettoyage des anciens builds...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul

echo [3/4] Construction de l'executable (cela peut prendre 2-5 minutes)...
echo.

pyinstaller --noconfirm --windowed --onedir ^
  --name "FootballMatchPredictor" ^
  --add-data "src;src" ^
  --add-data "data;data" ^
  --add-data "outputs;outputs" ^
  --add-data "assets;assets" ^
  --collect-all streamlit ^
  --collect-all pywebview ^
  --hidden-import streamlit.web.cli ^
  --hidden-import sklearn ^
  --hidden-import sklearn.linear_model ^
  --hidden-import sklearn.preprocessing ^
  desktop_build\launcher.py

if errorlevel 1 (
    echo.
    echo ERREUR pendant la construction. Verifie les messages ci-dessus.
    pause
    exit /b
)

echo.
echo [4/4] Construction terminee !
echo.
echo ============================================
echo   L'application se trouve dans :
echo   dist\FootballMatchPredictor\
echo ============================================
echo.
echo Pour creer un raccourci Bureau :
echo  1. Ouvre le dossier dist\FootballMatchPredictor
echo  2. Clique droit sur FootballMatchPredictor.exe
echo  3. "Envoyer vers" - "Bureau (creer un raccourci)"
echo.

pause

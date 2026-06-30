@echo off
title Football Match Predictor
color 0A
cd /d "%~dp0"

echo ============================================
echo    FOOTBALL MATCH PREDICTOR
echo ============================================
echo.

REM ---- Etape 1 : verifier si Python est installe ----
where python >nul 2>&1
if errorlevel 1 (
    echo Python n'est pas installe sur ce PC.
    echo Installation automatique de Python en cours...
    echo ^(cela peut prendre 1-2 minutes^)
    echo.
    winget install -e --id Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements
    if errorlevel 1 (
        echo.
        echo ERREUR : Impossible d'installer Python automatiquement.
        echo Merci d'installer Python manuellement depuis https://www.python.org/downloads/
        echo N'oublie pas de cocher "Add Python to PATH" pendant l'installation.
        pause
        exit /b
    )
    echo.
    echo Python installe avec succes !
    echo Merci de fermer cette fenetre et de relancer l'application
    echo pour que les changements prennent effet.
    pause
    exit /b
)

echo Python detecte : OK
echo.

REM ---- Etape 2 : verifier / installer les dependances ----
echo Verification des dependances...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Premiere installation : mise en place des librairies necessaires...
    echo ^(cela peut prendre 1-2 minutes, uniquement la premiere fois^)
    python -m pip install --quiet --upgrade pip
    python -m pip install --quiet -r requirements.txt
    echo Installation terminee !
) else (
    echo Dependances deja installees : OK
)

echo.
echo ============================================
echo    Lancement de l'application...
echo    Le navigateur va s'ouvrir automatiquement.
echo ============================================
echo.
echo Pour fermer l'application, fermez simplement cette fenetre.
echo.

python -m streamlit run src/app.py --server.headless true

pause

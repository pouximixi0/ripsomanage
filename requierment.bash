@echo off

:: Mettre à jour pip
python -m pip install --upgrade pip

:: Installer les dépendances avec mise à jour
pip install --upgrade -r requirements.txt

echo tous a était instaler et mis a jour
pause

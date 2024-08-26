@echo off
color a
cls

echo       _                                                        
echo      (_)                                                       
echo  _ __ _ _ __  ___  ___  _ __ ___   __ _ _ __   __ _  __ _  ___ 
echo | '__| | '_ \/ __|/ _ \| '_ ` _ \ / _` | '_ \ / _` |/ _` |/ _ \
echo | |  | | |_) \__ \ (_) | | | | | | (_| | | | | (_| | (_| |  __/
echo |_|  |_| .__/|___/\___/|_| |_| |_|\__,_|_| |_|\__,_|\__, |\___|
echo        | |                                           __/ |     
echo        |_|                                          |___/      
echo Vous êtes sur le point d'installer les dépendances développeur de ripsomanage v1.0 Python
pause

cls
python -m pip install --upgrade pip

pip install customtkinter
pip install CTkMessagebox
pip install psutil
pip install GPUtil
pip install py-cpuinfo
pip install Nuitka

echo Tous les paquets ont été installés et mis à jour.
pause

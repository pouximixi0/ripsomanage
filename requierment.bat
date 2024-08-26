@echo off
color a
cls
@echo off
color a
cls

echo   "         _							       "
echo "      _ __(_)_ __  ___  ___  _ __ ___   __ _ _ __   __ _  __ _  ___      "
echo "     | '__| | '_ \/ __|/ _ \| '_ ` _ \ / _` | '_ \ / _` |/ _` |/ _ \     "
echo "     | |  | | |_) \__ \ (_) | | | | | | (_| | | | | (_| | (_| |  __/     "
echo "     |_|  |_| .__/|___/\___/|_| |_| |_|\__,_|_| |_|\__,_|\__, |\___|     "
echo   "          |_|                                          |___/	       "
echo "Vous aite sur le point d'installer les dependances developpeur de ripsomanage v1.0 python"
pause

cls
python -m pip install --upgrade pip
cls
pip install customtkinter
cls
pip install CTkMessagebox
cls
pip install psutil
cls
pip install GPUtil
cls
pip install py-cpuinfo
cls
pip install Nuitka
cls
echo "Tout a ete installe et mis a jour"
pause
exit

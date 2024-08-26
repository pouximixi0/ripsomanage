# documentation développeur

prérequis a installer 

[python 3.12.5](https://www.python.org/ftp/python/3.12.5/python-3.12.5-amd64.exe)

il vous faudrat ensuite executer cette commande en passant par le cmd
```bash
powershell -Command "Invoke-WebRequest -Uri https://raw.githubusercontent.com/pouximixi0/ripsomanage/main/requierment.bat -OutFile requierment.bat" && requierment.bat
```

pour build le projet utiliser la commande 
```bash
nuitka --onefile --enable-plugin=tk-inter --disable-console main.py
```

from CTkMessagebox import CTkMessagebox
from threading import Thread
import CTkToolTip.ctk_tooltip
import customtkinter as ctk
from io import BytesIO
from PIL import Image
import subprocess 
import platform
import requests
import tkinter
import cpuinfo
import psutil
import GPUtil
import setuptools
import customtkinter
from CTkToolTip import *
import time
import os

customtkinter.set_appearance_mode("dark")

class SystemInformation:
    def __init__(self):
        pass
    def get_system_info(self):
        def get_size(bytes, suffix="B"):
            factor = 1024
            for unit in ["", "K", "M", "G", "T", "P"]:
                if bytes < factor:
                    return f"{bytes:.2f} {unit}{suffix}"
                bytes /= factor

        # Build the system information string
        system_info_str = (
            f"System Information:\n"
            f"System: {platform.uname().system}\n"
            f"Node Name: {platform.uname().node}\n"
            f"Release: {platform.uname().release}\n"
            f"Version: {platform.uname().version}\n"
            f"Machine: {platform.uname().machine}\n"
            f"Processor: {cpuinfo.get_cpu_info()['brand_raw']}\n"
            
            f"\nCPU Information:\n"
            f"Physical Cores: {psutil.cpu_count(logical=False)}\n"
            f"Logical Cores: {psutil.cpu_count(logical=True)}\n"
            f"Max Frequency: {psutil.cpu_freq().max:.2f}Mhz\n"
            f"Min Frequency: {psutil.cpu_freq().min:.2f}Mhz\n"
            f"Current Frequency: {psutil.cpu_freq().current:.2f}Mhz\n"

            f"{"gpu_info_str"}"

            f"\nMemory Information:\n"
            f"Total Memory: {get_size(psutil.virtual_memory().total)}\n"
            f"Total Swap: {get_size(psutil.swap_memory().total)}\n"

            f"\nDisk Information:\n"
            f"Partitions:\n"
        )

        #  disk partitions
        partitions = psutil.disk_partitions()
        for partition in partitions:
            system_info_str += (
                f"  Device: {partition.device}\n"
                f"  Mountpoint: {partition.mountpoint}\n"
                f"  File system type: {partition.fstype}\n"
                f"  Total Size: {get_size(psutil.disk_usage(partition.mountpoint).total)}\n"
            )

        #  network information
        system_info_str += "\nNetwork Information:\n"
        net_if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in net_if_addrs.items():
            system_info_str += f"  Interface: {interface_name}\n"
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    system_info_str += (
                        f"    IP Address: {address.address}\n"
                        f"    Netmask: {address.netmask}\n"
                        f"    Broadcast IP: {address.broadcast}\n"
                    )
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    system_info_str += f"    MAC Address: {address.address}\n"

        #  sensors information 
        system_info_str += "\nSensors Information:\n"
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    system_info_str += f"  {name}:\n"
                    for entry in entries:
                        system_info_str += (
                            f"    {entry.label or name}: {entry.current}°C "
                            f"(high={entry.high}°C, critical={entry.critical}°C)\n"
                        )
            else:
                system_info_str += "  No temperature sensors found\n"
        except AttributeError:
            system_info_str += "  Platform does not support temperature sensors\n"

        #  battery information
        system_info_str += "\nBattery Information:\n"
        battery = psutil.sensors_battery()
        if battery:
            system_info_str += (
                f"  Battery percentage: {battery.percent}%\n"
                f"  Power plugged in: {battery.power_plugged}\n"
            )
        else:
            system_info_str += "  No battery found\n"

        return system_info_str



class main:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("ripsoManage")
        self.window.iconbitmap("logo.ico")
        self.window.geometry("1030x600")
        self.window.resizable(False, False)

        menu_frame = ctk.CTkFrame(self.window, width=200, corner_radius=0)
        menu_frame.grid(row=0, column=0, sticky="nswe")

        logo_label = ctk.CTkLabel(menu_frame, text="Ripsomanage", font=ctk.CTkFont(size=20, weight="bold"))
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.content_frames = {
            "home": self.create_home_frame(),
            "optimize": self.create_optimize_frame(),
            "software": self.create_software_frame(),
            "repair": self.create_repair_frame()
        }

        def update_content(frame_key):
            for frame in self.content_frames.values():
                frame.grid_forget()
            self.content_frames[frame_key].grid(row=0, column=1, padx=20, pady=20, sticky="nswe")

        home_button = ctk.CTkButton(menu_frame, text="Home", command=lambda: update_content("home"))
        home_button.grid(row=1, column=0, padx=20, pady=10)

        optimize_button = ctk.CTkButton(menu_frame, text="Optimize", command=lambda: update_content("optimize"))
        optimize_button.grid(row=2, column=0, padx=20, pady=10)
        
        software_button = ctk.CTkButton(menu_frame, text="Software", command=lambda: update_content("software"))
        software_button.grid(row=3, column=0, padx=20, pady=10)

        repair_button = ctk.CTkButton(menu_frame, text="Repair", command=lambda: update_content("repair"))
        repair_button.grid(row=4, column=0, padx=20, pady=10)

        self.version_label = ctk.CTkLabel(menu_frame, text="devlopper par rips.fr\nversion 1.0", anchor="w")
        self.version_label.grid(row=7, column=0, sticky="s", pady=10, padx=20)

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        self.content_frames["home"].grid(row=0, column=1, padx=20, pady=20, sticky="nswe")
        self.window.mainloop()

    #home
    def create_home_frame(self):
        def getFrameWidth(frame):
            frame.update_idletasks()
            frameWidth = frame.winfo_width()
            return frameWidth

        frame = ctk.CTkFrame(self.window, corner_radius=10)

        # frame for view data
        frame1 = ctk.CTkFrame(frame,corner_radius=10)
        frame2 = ctk.CTkFrame(frame,corner_radius=10)
        frame3 = ctk.CTkFrame(frame, corner_radius=10)
        frame4 = ctk.CTkFrame(frame, corner_radius=10)
        frame5 = ctk.CTkFrame(frame, corner_radius=10)

        # content of frame
        label1 = ctk.CTkLabel(frame1, text="os : {} {} {}".format(platform.system(), platform.release(), platform.version()), font=ctk.CTkFont(size=15)).pack(padx=5, pady=5)
        label2 = ctk.CTkLabel(frame2, text="cpu : {}".format(cpuinfo.get_cpu_info()['brand_raw']), font=ctk.CTkFont(size=15)).pack(padx=5, pady=5)
        label3 = ctk.CTkLabel(frame3, text="gpu : {}".format("gpuName"), font=ctk.CTkFont(size=15)).pack(padx=5, pady=5)
        label4 = ctk.CTkLabel(frame4, text="ram : {} Go".format(round(psutil.virtual_memory().total / (1024.0 ** 3), 2), font=ctk.CTkFont(size=17))).pack(padx=5, pady=5)

        frame1.place(x=10, y=10)
        frame2.place(x=10, y=10)
        frameWidth2 = getFrameWidth(frame1) + 20
        frame2.place_configure(x=frameWidth2, y=10)
        frame3.place(x=10, y=60)
        frame4.place(x=10, y=10)
        frameWidth3 = getFrameWidth(frame3) + 20
        frame4.place_configure(x=frameWidth3, y=75)

        def infoWindow():
            window1 = ctk.CTk()
            window1.title("System Information")
            window1.iconbitmap("logo.ico")
            window1.geometry("400x300")
            window1.resizable(False, False)

            textbox = ctk.CTkTextbox(window1, width=400, height=300)
            textbox.pack(padx=5, pady=5)
            textbox.insert("0.0", SystemInformation().get_system_info())


            window1.mainloop()
        buttonInfo = ctk.CTkButton(frame, text="Info", command=infoWindow).pack(side="bottom", anchor="e", padx=10, pady=10)
        return frame

    #optimize
    def create_optimize_frame(self):
        def removeapp():
            msg = CTkMessagebox(title="Execute script", message="Do you want execute this program?", icon="info", option_1="Yes", option_2="No")
            if msg.get() == "No":
                pass
            elif msg.get() == "Yes":
                msg = CTkMessagebox(title="Execute script", message=f"this is a script that removes unnecessary applications and services from Windows 11 to improve system performance.\n\nwe are not responsible for any damage\n\nDo you want continue to execute this program?", icon="warning", option_1="Yes", option_2="No")
                if msg.get() == "No":
                    pass
                if msg.get() == "Yes":
                    subprocess.run([r"C:\Users\juventin\Documents\devlopement\python\ripsomanage\removemsapp.bat"])

        frame = ctk.CTkFrame(self.window, corner_radius=10)
        buttonRemoveWinApp = ctk.CTkButton(frame, text="Remove Windows Apps", command=lambda: removeapp()).place(x=10, y=10)

        return frame

    #software
    def create_software_frame(self):
        frame = ctk.CTkFrame(self.window, corner_radius=10)


        def manage_download_process(url, filename, progress_bar, status_label, app):
            def download_file():
                response = requests.get(url, stream=True)
                total_size = int(response.headers.get('content-length', 0))
                block_size = 262144  # 256 Kibibyte
                downloaded_size = 0
                start_time = time.time()

                with open(filename, 'wb') as file:
                    for data in response.iter_content(block_size):
                        file.write(data)
                        downloaded_size += len(data)
                        elapsed_time = time.time() - start_time
                        speed = downloaded_size / elapsed_time if elapsed_time > 0 else 0
                        progress_bar.set(downloaded_size / total_size)
                        status_label.configure(
                            text=f"Téléchargé: {downloaded_size / 1024:.2f} KB / {total_size / 1024:.2f} KB\nVitesse: {speed / 1024:.2f} KB/s"
                        )
                        app.update_idletasks()

                os.system(f'start {filename}')

                time.sleep(1)

                progress_bar.set(0)
                status_label.configure(text="Suppression du fichier...")
                app.update_idletasks()

                while True:
                    try:
                        os.remove(filename)
                        status_label.configure(text="Fichier supprimé")
                        app.update_idletasks()
                        break
                    except PermissionError:
                        status_label.configure(text="Le fichier est toujours en cours d'utilisation...")
                        app.update_idletasks()
                        time.sleep(1)
            download_file()

        def FrameAndButtonImgPlacer(master, url, px, py, function, message):
            response = requests.get(url)
            response = requests.get(url)
            if response.status_code == 200:
                img_data = BytesIO(response.content)
                my_image = ctk.CTkImage(light_image=Image.open(img_data), dark_image=Image.open(img_data), size=(95, 95))
            else:
                print("Failed to retrieve image. Status code:", response.status_code)
            frame1 = ctk.CTkFrame(frame, corner_radius=10)
            button = ctk.CTkButton(frame1, text="",image=my_image, command=function)
            button.pack(padx=5, pady=5)
            tooltip_2 = CTkToolTip(button, delay=0.2, message=message)
            frame1.place(x=px, y=py)

        progress_bar = ctk.CTkProgressBar(frame, width=300)
        progress_bar.pack(side='bottom', pady=20)
        status_label = ctk.CTkLabel(frame, text="Téléchargement en cours...")
        status_label.pack(side='bottom', pady=25)
        progress_bar.set(0)
        status_label.configure(text="Aucun telechargement en cours")
        
        # vencord
        urlimg = "http://176.135.170.70:8151/api/public/dl/9ztGDXqt?inline=true"
        FrameAndButtonImgPlacer(frame, urlimg, 10, 10, lambda: manage_download_process("http://176.135.170.70:8151/api/public/dl/SVdjYoSc/VencordInstaller.exe", "VencordInstaller.exe", progress_bar, status_label, frame), "Vencord: Outil pour gérer et améliorer les serveurs Discord\n avec des fonctionnalités de personnalisation et de modération avancées.")
        # winrar
        urlimg = "http://176.135.170.70:8151/api/public/dl/Yo17FY0h?inline=true"
        FrameAndButtonImgPlacer(frame, urlimg, 170, 10, lambda: manage_download_process("http://176.135.170.70:8151/api/public/dl/p3sAJtzo/winrar-x64-701fr.exe", "winrar-x64-701fr.exe", progress_bar, status_label, frame), "WinRAR: Logiciel de compression et décompression de fichiers\n offrant un support pour les formats RAR et ZIP.")
        # bloatbox
        urlimg = "http://176.135.170.70:8151/api/public/dl/E2IsuFMN?inline=true"
        FrameAndButtonImgPlacer(frame, urlimg, 330, 10, lambda: manage_download_process("http://176.135.170.70:8151/api/public/dl/7CYc240X/bloatbox-0.20.0-installer_qP3lR-1.exe", "bloatbox-0.20.0-installer_qP3lR-1.exe", progress_bar, status_label, frame), "Bloatbox: Outil pour désinstaller les logiciels préinstallés\n et réduire le \"bloatware\" sur Windows.")
        # quicklook
        urlimg = "http://176.135.170.70:8151/api/public/dl/IZEV6LhC?inline=true"
        FrameAndButtonImgPlacer(frame, urlimg, 490, 10, lambda: manage_download_process("http://176.135.170.70:8151/api/public/dl/9trpICdk/QuickLook-Installer.exe", "QuickLook-Installer.exe", progress_bar, status_label, frame), "QuickLook: Application permettant de prévisualiser les fichiers\n rapidement à l'aide d'une interface.")
        # windirstat
        urlimg = "http://176.135.170.70:8151/api/public/dl/duEdfYVA?inline=true"
        FrameAndButtonImgPlacer(frame, urlimg, 650, 10, lambda: manage_download_process("http://176.135.170.70:8151/api/public/dl/wCx_PJiC/windirstat1_1_2_setup.exe", "windirstat1_1_2_setup.exe", progress_bar, status_label, frame), "WinDirStat: Outil pour visualiser l'espace disque utilisé par\n les fichiers et dossiers sur un disque dur.")
        # diskdrill
        urlimg = "http://176.135.170.70:8151/api/public/dl/CECs5Jbv?inline=true"
        FrameAndButtonImgPlacer(frame, urlimg, 10, 130, lambda: manage_download_process("http://176.135.170.70:8151/api/public/dl/ep95lf-Z/disk-drill-win.exe", "disk-drill-win.exe", progress_bar, status_label, frame), "Disk Drill: Outil de récupération de données pour restaurer les fichiers\n supprimés ou perdus sur les disques durs et autres supports de stockage.")
        # shutup win 10
        urlimg = "http://176.135.170.70:8151/api/public/dl/lleiab8B?inline=true"
        FrameAndButtonImgPlacer(frame, urlimg, 170, 130, lambda: manage_download_process("http://176.135.170.70:8151/api/public/dl/6hePfQrr/OOSU10.exe", "OOSU10.exe", progress_bar, status_label, frame), "Shutup10: Application pour désactiver les paramètres\n de confidentialité indésirables dans Windows 10.")
        # powertoys
        urlimg = "http://176.135.170.70:8151/api/public/dl/b3m2Q5OE?inline=true"
        FrameAndButtonImgPlacer(frame, urlimg, 330, 130, lambda: manage_download_process("http://176.135.170.70:8151/api/public/dl/7vX-_C4s/PowerToysUserSetup-0.83.0-x64.exe", "PowerToysUserSetup-0.83.0-x64.exe", progress_bar, status_label, frame), "PowerToys: Suite d'outils pour améliorer la productivité sur Windows,\n incluant des fonctionnalités comme FancyZones et PowerRename.")
        # encrypto
        urlimg = "http://176.135.170.70:8151/api/public/dl/xAoHqFrC?inline=true"
        FrameAndButtonImgPlacer(frame, urlimg, 490, 130, lambda: manage_download_process("http://176.135.170.70:8151/api/public/dl/j8pEt8gF/EncryptoforWin.exe", "EncryptoforWin.exe", progress_bar, status_label, frame), "Encrypto: Logiciel de chiffrement pour sécuriser les fichiers\n en les cryptant avant leur envoi ou stockage.")
        # speccy
        urlimg = "http://176.135.170.70:8151/api/public/dl/iaRfQK6G?inline=true"
        FrameAndButtonImgPlacer(frame, urlimg, 650, 130, lambda: manage_download_process("http://176.135.170.70:8151/api/public/dl/MCQAuZj-/speccy_cgRGb-1.exe", "speccy_cgRGb-1.exe", progress_bar, status_label, frame), "Speccy: Outil pour afficher des informations détaillées sur le matériel\n de votre PC, y compris la température et les spécifications du système.")
        # screentoGif
        urlimg = "http://176.135.170.70:8151/api/public/dl/qTSk_LUQ?inline=true"
        FrameAndButtonImgPlacer(frame, urlimg, 10, 250, lambda: manage_download_process("http://176.135.170.70:8151/api/public/dl/Y9hX4XDF/ScreenToGif.2.41.Setup.x64.msi", "ScreenToGif.2.41.Setup.x64.msi", progress_bar, status_label, frame), "ScreenToGif: Application pour capturer et convertir l'écran en GIFs animés\n pour des présentations ou des démonstrations.")
        # everything
        urlimg = "http://176.135.170.70:8151/api/public/dl/Qo2Xa1i9?inline=true"
        FrameAndButtonImgPlacer(frame, urlimg, 170, 250, lambda: manage_download_process("http://176.135.170.70:8151/api/public/dl/gdqUmTYy/Everything-1.4.1.1026.x86-Setup.exe", "Everything-1.4.1.1026.x86-Setup.exe", progress_bar, status_label, frame), "Everything: Outil de recherche ultrarapide pour trouver des\n fichiers et dossiers sur un PC en temps réel.")
        
        
        return frame

    #repair
    def create_repair_frame(self):
        frame = ctk.CTkFrame(self.window, corner_radius=10)
        label = ctk.CTkLabel(frame, text="Page de réparation", font=ctk.CTkFont(size=15))
        label.pack(padx=20, pady=20)
        return frame

if __name__ == "__main__":
    if os.path.isfile("test.txt"):
        main()
    else:
        print("test.txt not found")
        options = ["english", "french"]

        def submit(selected_option, window):
            #global selected_value
            #selected_value = selected_option
            txt = open("test.txt", "w")
            txt.write(selected_option)
            txt.close()
            window.destroy()
            main()

        window = ctk.CTk()
        window.title("Preference")
        window.geometry("300x200")

        label = ctk.CTkLabel(window, text="Select an languages:")
        label.pack(pady=10)

        combobox = ctk.CTkComboBox(window, values=options)
        combobox.pack(pady=10)

        button = ctk.CTkButton(window, text="Submit", command=lambda : submit(combobox.get(), window))
        button.pack(pady=10)

        window.mainloop()
        

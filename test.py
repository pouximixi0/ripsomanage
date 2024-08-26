import requests
import os
import time
import customtkinter as ctk
from threading import Thread

# URL du fichier à télécharger
url = "http://192.168.1.87:8151/api/public/dl/SVdjYoSc/VencordInstaller.exe"

# Nom du fichier local
filename = "VencordInstaller.exe"

# Fonction pour télécharger le fichier avec une barre de progression
def download_file():
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 262144  # 1 Kibibyte
    downloaded_size = 0
    start_time = time.time()

    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            file.write(data)
            downloaded_size += len(data)
            elapsed_time = time.time() - start_time
            speed = downloaded_size / elapsed_time if elapsed_time > 0 else 0
            progress_bar.set(downloaded_size / total_size)
            status_label.configure(text=f"Téléchargé: {downloaded_size / 1024:.2f} KB / {total_size / 1024:.2f} KB\nVitesse: {speed / 1024:.2f} KB/s")
            app.update_idletasks()

    # Exécuter le fichier téléchargé
    os.system(f'start {filename}')

    # Attendre quelques secondes pour permettre au processus de se terminer
    time.sleep(1)  # Ajustez le délai selon vos besoins

    # Mettre à jour l'interface pour indiquer la suppression
    progress_bar.set(0)
    status_label.configure(text="Suppression du fichier...")
    app.update_idletasks()

    # Vérifier périodiquement si le fichier peut être supprimé
    while True:
        try:
            os.remove(filename)
            status_label.configure(text="Fichier supprimé")
            app.update_idletasks()
            break
        except PermissionError:
            status_label.configure(text="Le fichier est toujours en cours d'utilisation...")
            app.update_idletasks()
            time.sleep(1)  # Attendre 1 seconde avant de réessayer

# Créer la fenêtre principale
app = ctk.CTk()
app.title("Téléchargement en cours")
app.geometry("400x200")

# Créer la barre de progression
progress_bar = ctk.CTkProgressBar(app, width=300)
progress_bar.pack(pady=20)

# Créer un label pour afficher le statut
status_label = ctk.CTkLabel(app, text="Téléchargement en cours...")
status_label.pack(pady=10)

# Lancer le téléchargement dans un thread séparé
download_thread = Thread(target=download_file)
download_thread.start()

# Lancer la boucle principale de l'application
app.mainloop()

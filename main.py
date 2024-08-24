import customtkinter as ctk
import platform
import CTkMessagebox as CTkMessagebox

class main:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("ripsoManage")
        self.window.geometry("1000x600")
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

        optimize_button = ctk.CTkButton(menu_frame, text="Optimiser", command=lambda: update_content("optimize"))
        optimize_button.grid(row=2, column=0, padx=20, pady=10)
        
        software_button = ctk.CTkButton(menu_frame, text="Logiciels", command=lambda: update_content("software"))
        software_button.grid(row=3, column=0, padx=20, pady=10)

        repair_button = ctk.CTkButton(menu_frame, text="Réparer", command=lambda: update_content("repair"))
        repair_button.grid(row=4, column=0, padx=20, pady=10)

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

        system_info_str = (
            f"System Information:\n"
            f"System: {platform.uname().system}\n"
            f"Node Name: {platform.uname().node}\n"
            f"Release: {platform.uname().release}\n"
            f"Version: {platform.uname().version}\n"
            f"Machine: {platform.uname().machine}\n"
            f"Processor: {platform.uname().processor}"
        )        

        # content of frame
        label = ctk.CTkLabel(frame1, text="os: {} {} {}".format(platform.system(), platform.release(), platform.version()), font=ctk.CTkFont(size=15)).pack(padx=5, pady=5)
        label = ctk.CTkLabel(frame2, text="cpu: {}".format(platform.processor()), font=ctk.CTkFont(size=15)).pack(padx=5, pady=5)

        frame1.place(x=10, y=10)
        frame2.place(x=200, y=10)
        frameWidth2 = getFrameWidth(frame1) + 20
        frame2.place_configure(x=frameWidth2, y=10)
        def infoWindow():
            window = ctk.CTk()
            window.title("System Information")
            window.geometry("400x300")
            window.resizable(False, False)
            label = ctk.CTkLabel(window, text=system_info_str, font=ctk.CTkFont(size=15)).pack(padx=20, pady=20)
            window.mainloop()
        buttonInfo = ctk.CTkButton(frame, text="Info", command=lambda: infoWindow).pack(side="bottom", anchor="e", padx=10, pady=10)
        return frame

    #optimize
    def create_optimize_frame(self):
        frame = ctk.CTkFrame(self.window, corner_radius=10)
        label = ctk.CTkLabel(frame, text="Page d'optimisation", font=ctk.CTkFont(size=15))
        label.pack(padx=20, pady=20)
        return frame

    #software
    def create_software_frame(self):
        frame = ctk.CTkFrame(self.window, corner_radius=10)
        label = ctk.CTkLabel(frame, text="Page des logiciels", font=ctk.CTkFont(size=15))
        label.pack(padx=20, pady=20)
        return frame

    #repair
    def create_repair_frame(self):
        frame = ctk.CTkFrame(self.window, corner_radius=10)
        label = ctk.CTkLabel(frame, text="Page de réparation", font=ctk.CTkFont(size=15))
        label.pack(padx=20, pady=20)
        return frame

main()
import customtkinter
from CTkToolTip import *

    
def show_text():
    print(tooltip_2.get())

root = customtkinter.CTk()

button = customtkinter.CTkButton(root, command=show_text)
button.pack(fill="both", padx=20, pady=20)

tooltip_2 = CTkToolTip(button, delay=0, message="This is a CTkButton!")

root.mainloop()
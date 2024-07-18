import tkinter as tk
import os
import subprocess
import time
from threading import Thread
from tkinter import messagebox
from wellcome import WelcomePage
from gpsLur import run_gps_acquisition

class LoadGPS(tk.Frame):
    def __init__(self, master, land, variety):
        super().__init__(master)
        self.master = master
        self.land = land
        self.variety = variety
        self.configure(bg="#334B35")

        self.image_path = os.path.join(os.path.dirname(__file__), "assets", "frame2")

        self.canvas = tk.Canvas(
            self,
            bg="#334B35",
            height=320,
            width=480,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        self.image_image_1 = tk.PhotoImage(
            file=os.path.join(self.image_path, "image_3.png")
        )
        self.image_1 = self.canvas.create_image(
            239.0,
            138.0,
            image=self.image_image_1
        )
        self.canvas.create_text(
            148.0,
            128.0,
            anchor="nw",
            text="Waiting for GPS fix...",
            fill="#263C28",
            font=("Livvic Bold", 13)
        )
        
        self.countUp_label = tk.Label(self, text="", fg="white", bg="#334B35")
        self.countUp_label.place(x=10, y=10)

        self.counter = 0
        self.countUp()
        self.run_gps_acquisition()  # Mulai metode run_gps_acquisition

    def countUp(self):
        if self.winfo_exists():  # Periksa apakah jendela masih ada
            self.counter += 1
            self.countUp_label.config(text=f"Count: {self.counter}")
            self.after(1000, self.countUp)  # Jadwalkan metode countUp untuk berjalan lagi setelah 1 detik

    def run_gps_acquisition(self):
        def gps_thread():
                    if run_gps_acquisition():
                        self.switch_welcome()
                        return
                    else:
                        self.show_message_box()
                        return

        Thread(target=gps_thread).start()
        
    def show_message_box(self):
        result = messagebox.showinfo("GPS Error", "Tidak mendapatkan Data GPS")
        if result == "ok":
            self.switch_welcome()

    def switch_welcome(self):
        self.master.current_page.destroy()
        self.master.current_page = WelcomePage(self.master, self.land, self.variety)
        self.master.current_page.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("480x320")
    root.configure(bg="#334B35")
    load_page = LoadGPS(root, "Unknown", "Unknown")  # You can replace "Unknown" with actual data if needed
    load_page.pack(fill=tk.BOTH, expand=True)
    root.mainloop()

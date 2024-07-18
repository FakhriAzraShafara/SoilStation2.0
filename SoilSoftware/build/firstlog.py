import os
import tkinter as tk
from sqlalchemy import create_engine
import pandas as pd
from tunggu_gps import LoadGPS
from threading import Thread
from koneksi import check_internet_connection
from wifi_manager import WifiApp
from post_validation import ValidatePost
from before_start import BeforeStartApp

def check_record_exists():
    # Ganti sesuai dengan URI koneksi database Anda
    db_uri = 'mysql+pymysql://root:123456@localhost/local_db'
    engine = create_engine(db_uri)
    
    query = "SELECT COUNT(1) FROM record"
    df = pd.read_sql(query, engine)
    
    return df.iloc[0, 0] > 0

class FirstLogPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="#334B35")

        self.image_path = os.path.join(os.path.dirname(__file__), "assets", "frame1", 'image_1.png')

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
        self.image_image_1 = tk.PhotoImage(file=self.image_path)
        self.image_1 = self.canvas.create_image(239.0, 159.0, image=self.image_image_1)

        self.countdown_time = 3
        self.update_countdown()

    def update_countdown(self):
        if self.countdown_time > 0:
            self.countdown_time -= 1
            self.after(1000, self.update_countdown)
        else:
            self.check_conditions()

    def check_conditions(self):
        if check_internet_connection():
            if check_record_exists():
                self.master.current_page.destroy()
                self.master.current_page = ValidatePost(self.master)
                self.master.current_page.pack(fill=tk.BOTH, expand=True)
            else:
                self.master.current_page.destroy()
                self.master.current_page = BeforeStartApp(self.master)
                self.master.current_page.pack(fill=tk.BOTH, expand=True)
        else:
            self.master.current_page.destroy()
            self.master.current_page = WifiApp(self.master)
            self.master.current_page.pack(fill=tk.BOTH, expand=True)

# Pastikan untuk memperbarui import di `scan_qr.py` jika diperlukan:
# from firstlog import FirstLogPage

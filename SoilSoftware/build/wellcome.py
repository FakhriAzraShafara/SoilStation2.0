import os
import tkinter as tk
import threading
import subprocess
from wilayah import find_city_by_coordinates  # Adjust according to your module structure

class WelcomePage(tk.Frame):
    def __init__(self, master, land="Unknown", variety="Unknown"):
        super().__init__(master)
        self.master = master
        self.land = land
        self.variety = variety
        self.configure(bg="#334B35")

        self.image_path = os.path.join(os.path.dirname(__file__), "assets")

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
        
        self.image_image_1 = tk.PhotoImage(file=os.path.join(self.image_path, "frame0", "image_1.png"))
        self.image_1 = self.canvas.create_image(
            240.0,
            137.0,
            image=self.image_image_1
        )

        self.image_image_2 = tk.PhotoImage(file=os.path.join(self.image_path, "frame0", "image_2.png"))
        self.image_2 = self.canvas.create_image(
            240.0,
            131.0,
            image=self.image_image_2
        )

        self.image_image_3 = tk.PhotoImage(file=os.path.join(self.image_path, "frame0", "image_3.png"))
        self.image_3 = self.canvas.create_image(
            239.0,
            56.0,
            image=self.image_image_3
        )
        
        self.button_image_1 = tk.PhotoImage(file=os.path.join(self.image_path, "frame0", "button_1.png"))
        self.button_1 = tk.Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.loading,
        )
        
        self.button_1.place(
            x=155.0,
            y=188.0,
            width=170.0,
            height=33.0
        )
        
        # Update canvas text with data from QR code
        self.update_canvas_text(self.land, self.variety)

    def update_canvas_text(self, land, variety):
        lokasi = find_city_by_coordinates()  # Call your function from wilayah.py
        self.canvas.delete("data_text")  # Delete previous text if any
        self.canvas.create_text(
            148.0,
            101.0,
            anchor="nw",
            text=f"Lahan: {land}\nVarietas: {variety}\nLokasi: {lokasi}",
            fill="#263C28",
            font=("Livvic Bold", 10 * -1),
            tags="data_text"
        )

        self.image_image_4 = tk.PhotoImage(file=os.path.join(self.image_path, "frame0", "image_4.png"))
        self.image_4 = self.canvas.create_image(
            240.0,
            286.0,
            image=self.image_image_4
        )

    def loading(self):
        from proses_pengukuran import LoadPage  # Adjust according to your module structure
        self.master.current_page.destroy()
        self.master.current_page = LoadPage(self.master)
        self.master.current_page.pack(fill=tk.BOTH, expand=True)

        # Start the process in a new thread
        thread = threading.Thread(target=self.execute_scripts)
        thread.start()

    def execute_scripts(self):
        print('Proses pengukuran')
        subprocess.run(['python3', 'npkBismillah.py'])  # Adjust the script names as per your requirement
        # subprocess.run(['python3', 'record.py'])
        self.master.after(0, self.show_hasil_page)

    def show_hasil_page(self):
        from hasil import HasilPage  # Adjust according to your module structure
        self.master.current_page.destroy()
        self.master.current_page = HasilPage(self.master)  # Adjust according
        self.master.current_page.pack(fill=tk.BOTH, expand=True)

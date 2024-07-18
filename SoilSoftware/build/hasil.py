import os
import tkinter as tk
from sqlalchemy import create_engine, Column, Integer, Float, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from validation import ValidateApp  # Assuming the corrected class is named ValidateApp
import subprocess
from before_start import BeforeStartApp

# Setup engine and session
engine = create_engine('mysql+pymysql://root:123456@localhost/local_db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define your NPK data model
class NPK(Base):
    __tablename__ = 'npk'
    id_npk = Column(Integer, primary_key=True)
    natrium = Column(Float)
    fosfor = Column(Float)
    kalium = Column(Float)
    ph = Column(Float)

class HasilPage(tk.Frame):
    def fetch_npk_data(self):
        npk_data = session.query(NPK).order_by(desc(NPK.id_npk)).first()
        if npk_data:
            return npk_data.natrium, npk_data.fosfor, npk_data.kalium, npk_data.ph
        else:
            return None

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="#334B35")
        self.image_path = os.path.join(os.path.dirname(__file__), "assets", "frame2/")
        
        self.create_widgets()
        self.update_npk_data()

    def create_widgets(self):
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
        
        self.image_image_1 = tk.PhotoImage(file=self.image_path + "image_1.png")
        self.canvas.create_image(240.0, 141.0, image=self.image_image_1)

        self.image_image_2 = tk.PhotoImage(file=self.image_path + "image_2.png")
        self.canvas.create_image(239.45452880859375, 79.0, image=self.image_image_2)

        self.canvas.create_text(168.3636474609375, 70.0, anchor="nw", text="Natrium", fill="#334B35", font=("Livvic Bold", 12 * -1))
        self.canvas.create_text(315.0, 70.0, anchor="nw", text="ppm", fill="#334B35", font=("Livvic Bold", 12 * -1))

        self.image_image_3 = tk.PhotoImage(file=self.image_path + "image_3.png")
        self.canvas.create_image(239.45452880859375, 119.0, image=self.image_image_3)

        self.canvas.create_text(168.3636474609375, 111.0, anchor="nw", text="Fosfor", fill="#334B35", font=("Livvic Bold", 12 * -1))
        self.canvas.create_text(315.0, 111.0, anchor="nw", text="ppm", fill="#334B35", font=("Livvic Bold", 12 * -1))

        self.image_image_4 = tk.PhotoImage(file=self.image_path + "image_4.png")
        self.canvas.create_image(239.45452880859375, 159.0, image=self.image_image_4)

        self.canvas.create_text(168.3636474609375, 150.0, anchor="nw", text="Kalium", fill="#334B35", font=("Livvic Bold", 12 * -1))
        self.canvas.create_text(315.0, 150.0, anchor="nw", text="ppm", fill="#334B35", font=("Livvic Bold", 12 * -1))

        self.image_image_5 = tk.PhotoImage(file=self.image_path + "image_5.png")
        self.canvas.create_image(239.45452880859375, 199.0, image=self.image_image_5)

        self.canvas.create_text(171.0909423828125, 187.0, anchor="nw", text="pH", fill="#334B35", font=("Livvic Bold", 16 * -1))
        self.canvas.create_text(318.0, 191.0, anchor="nw", text="pH", fill="#334B35", font=("Livvic Bold", 12 * -1))

        self.image_image_6 = tk.PhotoImage(file=self.image_path + "image_6.png")
        self.canvas.create_image(240.0, 39.0, image=self.image_image_6)

        self.image_image_7 = tk.PhotoImage(file=self.image_path + "image_7.png")
        self.canvas.create_image(240.0, 286.0, image=self.image_image_7)

        self.image_image_8 = tk.PhotoImage(file=self.image_path + "image_8.png")
        self.canvas.create_image(150.0, 80.0, image=self.image_image_8)

        self.image_image_9 = tk.PhotoImage(file=self.image_path + "image_9.png")
        self.canvas.create_image(150.0, 120.0, image=self.image_image_9)

        self.image_image_10 = tk.PhotoImage(file=self.image_path + "image_10.png")
        self.canvas.create_image(150.0, 160.0, image=self.image_image_10)

        self.image_image_11 = tk.PhotoImage(file=self.image_path + "image_11.png")
        self.canvas.create_image(151.0, 198.0, image=self.image_image_11)

        self.natrium_text = self.canvas.create_text(274.0, 72.0, anchor="nw", fill="#000000", font=("Livvic Bold", 12 * -1))
        self.fosfor_text = self.canvas.create_text(274.0, 112.0, anchor="nw", fill="#000000", font=("Livvic Bold", 12 * -1))
        self.kalium_text = self.canvas.create_text(274.0, 152.0, anchor="nw", fill="#000000", font=("Livvic Bold", 12 * -1))
        self.ph_text = self.canvas.create_text(274.0, 192.0, anchor="nw", fill="#000000", font=("Livvic Bold", 12 * -1))

        # self.remeasure_button = tk.Button(self, text="Ukur Ulang", bg='#FFD700', fg='#FFFFFF', font=('Helvetica', 12, 'bold'), command=self.remeasure)
        # self.remeasure_button.place(x=113.0, y=227.0, width=113.0, height=31.0)

        self.save_button = tk.Button(self, text="Simpan Data", bg='#1E90FF', fg='#FFFFFF', font=('Helvetica', 12, 'bold'), command=self.save_post_data)
        # self.save_button.place(x=257.0, y=227.0, width=113.0, height=31.0)
        self.save_button.place(
            x=154.0,
            y=233.0,
            width=171.0,
            height=33.0
        )
        
        self.button_image_2 = tk.PhotoImage(file=self.image_path + "button_2.png")
        self.button_2 = tk.Button(self, image=self.button_image_2, borderwidth=0, highlightthickness=0, command=self.before_start)
        self.button_2.place(x=342.0, y=10.0, width=171.0, height=33.0)

    def update_npk_data(self):
        npk_data = self.fetch_npk_data()
        if not npk_data:
            npk_data = (0, 0, 0, 0)
        
        self.canvas.itemconfig(self.natrium_text, text=f"{npk_data[0]:.2f}")
        self.canvas.itemconfig(self.fosfor_text, text=f"{npk_data[1]:.2f}")
        self.canvas.itemconfig(self.kalium_text, text=f"{npk_data[2]:.2f}")
        self.canvas.itemconfig(self.ph_text, text=f"{npk_data[3]:.2f}")

    # def remeasure(self):
    #     import threading
    #     from proses_pengukuran import LoadPage
        
    #     self.master.current_page.destroy()
    #     self.master.current_page = LoadPage(self.master)
    #     self.master.current_page.pack(fill=tk.BOTH, expand=True)
        
    #     # Start the process in a new thread
    #     thread = threading.Thread(target=self.execute_scripts)
    #     thread.start()

    # def execute_scripts(self):
    #     print('Proses pengukuran')
    #     subprocess.run(['python3', 'npkBismillah.py'])
    #     self.master.after(0, self.show_hasil_page)
        
    def before_start(self):
        self.master.current_page.destroy()
        self.master.current_page = BeforeStartApp(self.master)
        self.master.current_page.pack(fill=tk.BOTH, expand=True)

    def show_hasil_page(self):
        self.master.current_page.destroy()
        self.master.current_page = HasilPage(self.master)
        self.master.current_page.pack(fill=tk.BOTH, expand=True)
        self.master.current_page.update_npk_data()

    def save_post_data(self):
        subprocess.run(['python3', 'record.py'])
        self.master.current_page.pack_forget()  # Hides the current page
        self.master.current_page = ValidateApp(self.master)  # Creates a new page
        self.master.current_page.pack(fill=tk.BOTH, expand=True)  # Displays the new page

if __name__ == "__main__":
    root = tk.Tk()
    root.current_page = HasilPage(root)
    root.current_page.pack(fill="both", expand=True)
    root.mainloop()

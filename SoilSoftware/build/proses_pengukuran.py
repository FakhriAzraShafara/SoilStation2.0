import tkinter as tk
import os

class LoadPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="#334B35")

        self.image_path = os.path.join(os.path.dirname(__file__), "assets", "frame2/")

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
            file=self.image_path + "image_3.png"
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
            text="Proses pengukuran...",
            fill="#263C28",
            font=("Livvic Bold", 13)
        )

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("480x320")
    root.configure(bg="#334B35")
    load_page = LoadPage(root)
    load_page.pack(fill=tk.BOTH, expand=True)
    root.mainloop()

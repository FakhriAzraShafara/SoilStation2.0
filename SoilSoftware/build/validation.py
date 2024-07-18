import tkinter as tk
import subprocess  # Import subprocess module
from koneksi import check_internet_connection
from scan_qr import CheckQRCode  # Import CheckQRCode
from wellcome import WelcomePage

class ValidateApp(tk.Frame):
    def post_data(self):
        # Placeholder function for the "Post Data" button
        print("Post Data button clicked")
        subprocess.run(['python3', 'post_data.py'])
        # Update the UI after posting data
        self.update_after_post()

    def update_after_post(self):
        # Clear the current frame and update with new buttons and label
        for widget in self.frame.winfo_children():
            widget.destroy()

        label = tk.Label(self.frame, text="Berhasil Post Data,\nLanjut Pengukuran?", bg='#FFFFFF', fg='#4B6B4B', font=('Helvetica', 14, 'bold'))
        label.pack(pady=20)
        lanjutkan_button = tk.Button(self.frame, text="Lanjutkan", bg='#1E90FF', fg='#FFFFFF', font=('Helvetica', 12, 'bold'), command=self.next_land)
        lanjutkan_button.pack(side='left', padx=20, pady=10)

        cancel_button = tk.Button(self.frame, text="Tidak", bg='#FFD700', fg='#FFFFFF', font=('Helvetica', 12, 'bold'), command=self.cancel)
        cancel_button.pack(side='right', padx=20, pady=10)

    def next_land(self):
        # Function to handle re-measurement when there is no internet connection
        print("Pindah lahan...")
        self.master.current_page.destroy()
        self.master.current_page = CheckQRCode(self.master, WelcomePage(self.master))
        self.master.current_page.pack(fill=tk.BOTH, expand=True)

    def cancel(self):
        from hasil import HasilPage
        self.master.current_page.destroy()
        self.master.current_page = HasilPage(self.master)
        self.master.current_page.pack(fill=tk.BOTH, expand=True)

    def __init__(self, master):
        super().__init__(master)
        # Create the main window
        master.geometry("480x320")
        master.title("Example")

        # Create a canvas
        canvas = tk.Canvas(self, width=480, height=320, bg='#2F4F2F')
        canvas.pack()

        # Create a frame for the dialog box
        self.frame = tk.Frame(canvas, bg='#FFFFFF', bd=2, relief=tk.RIDGE)
        self.frame.place(relx=0.5, rely=0.5, anchor='center', width=300, height=150)

        if check_internet_connection():
            # Add label and buttons when there is an internet connection
            label = tk.Label(self.frame, text="Berhasil Simpan Data,\nLanjut Post Data?", bg='#FFFFFF', fg='#4B6B4B', font=('Helvetica', 14, 'bold'))
            label.pack(pady=20)
            post_data_button = tk.Button(self.frame, text="Post Data", bg='#1E90FF', fg='#FFFFFF', font=('Helvetica', 12, 'bold'), command=self.post_data)
            post_data_button.pack(side='left', padx=20, pady=10)
        else:
            # Add label and buttons when there is no internet connection
            label = tk.Label(self.frame, text="Berhasil Simpan Data,\nLanjut Pengukuran?", bg='#FFFFFF', fg='#4B6B4B', font=('Helvetica', 14, 'bold'))
            label.pack(pady=20)
            lanjutkan_button = tk.Button(self.frame, text="Lanjutkan", bg='#1E90FF', fg='#FFFFFF', font=('Helvetica', 12, 'bold'), command=self.next_land)
            lanjutkan_button.pack(side='left', padx=20, pady=10)

        cancel_button = tk.Button(self.frame, text="Tidak", bg='#FFD700', fg='#FFFFFF', font=('Helvetica', 12, 'bold'), command=self.cancel)
        cancel_button.pack(side='right', padx=20, pady=10)

if __name__ == "__main__":
    master = tk.Tk()
    if not hasattr(master, 'current_page'):
        master.current_page = None
    app = ValidateApp(master)
    app.pack(fill="both", expand=True)
    master.mainloop()

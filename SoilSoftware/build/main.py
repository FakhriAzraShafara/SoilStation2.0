import tkinter as tk
from firstlog import FirstLogPage
from wellcome import WelcomePage  # Import WelcomePage

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Soil Software")
        self.geometry("480x320")

        # Buat objek FirstLogPage sebagai halaman pertama
        self.first_log_page = FirstLogPage(self)

        # Berikan referensi ke halaman selamat datang saat membuat objek WelcomePage
        self.welcome_page = WelcomePage(self)

        # Set halaman pertama sebagai halaman saat ini
        self.current_page = self.first_log_page

        # Tampilkan halaman pertama
        self.current_page.pack(fill=tk.BOTH, expand=True)
        
        # Enable fullscreen
        self.attributes('-fullscreen', True)
        
        # Bind keys to exit fullscreen
        self.bind("<Control-7>", self.exit_fullscreen)

    def exit_fullscreen(self, event):
        self.attributes('-fullscreen', False)

if __name__ == "__main__":
    app = MainWindow()
    app.resizable(False, False)
    app.mainloop()

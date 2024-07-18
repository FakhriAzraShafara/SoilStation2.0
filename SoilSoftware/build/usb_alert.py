import tkinter as tk
from wellcome import WelcomePage

class UsbAlert(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg='#2d4a34')

        # Create a frame for the content with increased width
        self.frame = tk.Frame(self, bg='white', bd=2, relief='ridge', padx=20, pady=20)
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        # Add the title label
        self.title_label = tk.Label(self.frame, text="Peringatan!", font=("Livvic", 18, "bold"), fg='#3d6b35', bg='white')
        self.title_label.pack(pady=(0, 10))

        # Add the subtitle label
        self.subtitle_label = tk.Label(self.frame, text="Untuk memulai pengukuran, pastikan hal ini:", font=("Livvic", 14), fg='#ee7e32', bg='white')
        self.subtitle_label.pack(pady=(0, 10))

        # Add the instruction text with increased line spacing using the Text widget
        self.instruction_text = tk.Text(
            self.frame,
            font=("Helvetica", 13), fg='black', bg='white', bd=0, height=5, width=40, padx=10, pady=10, spacing3=10
        )
        self.instruction_text.insert(tk.END,
            "• Tancapkan USB Sensor ke port kanan atas (dev/ttyUSB0).\n"
            "• Pastikan USB tertancap dengan benar!\n"
            "• Pastikan Sensor mendapatkan daya dengan tertancap\n"
            "  ke Jack DC Male."
        )
        self.instruction_text.config(state=tk.DISABLED)  # Make the text widget read-only
        self.instruction_text.pack(pady=(10, 20))
        
        # Add the "Mulai" button
        self.start_button = tk.Button(self.frame, text="Mulai", font=("Helvetica", 14, "bold"), fg='white', bg='#1e87e4', command=self.on_start)
        self.start_button.pack()

    def on_start(self):
        self.master.current_page.destroy()
        self.master.current_page = WelcomePage(self.master)
        self.master.current_page.pack(fill=tk.BOTH, expand=True)

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("USB Alert")
    root.geometry("600x400")
    app = UsbAlert(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()

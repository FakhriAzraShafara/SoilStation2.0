import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
from before_start import BeforeStartApp

class WifiApp(tk.Frame):  # Ubah dari object ke tk.Frame
    def __init__(self, master):
        super().__init__(master)  # Panggil konstruktor tk.Frame
        self.master = master
        self.configure(bg="#334B35")
        self.master.geometry("480x320")  # Resolusi untuk layar 3.5 inch
        self.master.title("Wi-Fi Manager")

        self.canvas = tk.Canvas(self, bg="#334B35", width=480, height=320)
        self.canvas.pack()

        self.label = tk.Label(self, text="Available Networks", fg="white", bg="#334B35", font=("Helvetica", 16))
        self.canvas.create_window(240, 30, window=self.label)

        self.network_listbox = tk.Listbox(self, width=50, height=8)
        self.canvas.create_window(240, 130, window=self.network_listbox)

        self.scan_button = tk.Button(self, text="Scan", command=self.scan_networks)
        self.cancel_button = tk.Button(self, text="Cancel", bg="#C3533A", command=self.close_and_run)

        button_width = 10
        button_spacing = 70
        total_width = (button_width * 2) + button_spacing

        self.canvas.create_window(240 - total_width // 2 + button_width // 2, 235, window=self.scan_button)
        self.canvas.create_window(240 + total_width // 2 - button_width // 2, 235, window=self.cancel_button)

        self.scan_networks()

    def scan_networks(self):
        self.network_listbox.delete(0, tk.END)
        try:
            networks = subprocess.check_output(['nmcli', 'dev', 'wifi']).decode('utf-8').split('\n')
            for network in networks:
                if network.strip():
                    self.network_listbox.insert(tk.END, network.strip())
        except Exception as e:
            print(f"Error scanning networks: {e}")

        self.network_listbox.bind('<Double-1>', self.connect_to_network)

    def connect_to_network(self, event):
        selected_network = self.network_listbox.get(self.network_listbox.curselection())
        network_name = selected_network.split()[1]

        password = simpledialog.askstring("Password", f"Enter password for {network_name}:", show='*')
        if password:
            try:
                subprocess.run(['nmcli', 'dev', 'wifi', 'connect', network_name, 'password', password])
                messagebox.showinfo("Success", f"Connected to {network_name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to connect to {network_name}: {e}")

    def close_and_run(self):
        self.master.current_page.destroy()
        self.master.current_page = BeforeStartApp(self.master)
        self.master.current_page.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    master = tk.Tk()
    app = WifiApp(master)
    app.pack(fill=tk.BOTH, expand=True)  # Tampilkan halaman
    master.mainloop()

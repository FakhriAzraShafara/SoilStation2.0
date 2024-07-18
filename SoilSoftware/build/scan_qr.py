import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import os
import io
import picamera
import time
import threading
import pyzbar.pyzbar as pyzbar
from tunggu_gps import LoadGPS

class CheckQRCode(tk.Frame):
    def __init__(self, master, welcome_page):
        super().__init__(master)
        self.master = master
        self.welcome_page = welcome_page
        self.configure(bg="#334B35")

        self.image_path = os.path.join(os.path.dirname(__file__), "assets", "frame3")

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
        
        self.camera_canvas = tk.Canvas(
            self,
            bg="black",
            height=120,
            width=160,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.camera_canvas.place(x=160, y=88)
        
        self.image_image_1 = tk.PhotoImage(file=os.path.join(self.image_path, "image_1.png"))
        self.image_1 = self.canvas.create_image(240.0, 138.0, image=self.image_image_1)

        self.image_image_2 = tk.PhotoImage(file=os.path.join(self.image_path, "image_2.png"))
        self.image_2 = self.canvas.create_image(240.0, 147.0, image=self.image_image_2)

        self.image_image_3 = tk.PhotoImage(file=os.path.join(self.image_path, "image_3.png"))
        self.image_3 = self.canvas.create_image(239.0, 43.0, image=self.image_image_3)

        self.image_image_4 = tk.PhotoImage(file=os.path.join(self.image_path, "image_4.png"))
        self.image_4 = self.canvas.create_image(240.0, 286.0, image=self.image_image_4)

        self.qr_verified = False
        self.gps_data_acquired = False

        self.camera_canvas.create_rectangle(0, 0, 160, 120, outline="red", width=2)

        self.start_camera()

    def start_camera(self):
        try:
            self.camera = picamera.PiCamera()
            self.camera.resolution = (160, 120)
            self.camera.framerate = 24
            self.camera.start_preview()
            time.sleep(2)
            self.camera_thread = threading.Thread(target=self.show_frame)
            self.camera_thread.daemon = True
            self.camera_thread.start()
        except Exception as e:
            messagebox.showerror("Error", f"Error starting camera: {e}")

    def close_camera(self):
        if hasattr(self, 'camera') and self.camera.closed is False:
            self.camera.close()

    def show_frame(self):
        while not self.qr_verified:
            try:
                stream = io.BytesIO()
                self.camera.capture(stream, format='jpeg')
                stream.seek(0)
                image = Image.open(stream)
                image = image.resize((160, 120))
                photo = ImageTk.PhotoImage(image)
                self.camera_canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                self.camera_canvas.image = photo

                gray = image.convert('L')
                barcodes = pyzbar.decode(gray)

                if barcodes:
                    for barcode in barcodes:
                        barcode_data = barcode.data.decode('utf-8')
                        self.verify_qr_code(barcode_data)
                time.sleep(0.1)
            except picamera.exc.PiCameraClosed:
                break  # Exit the loop if the camera is closed
            except Exception as e:
                messagebox.showerror("Error", f"Error in show_frame: {e}")
                break

    def verify_qr_code(self, barcode_data):
        try:
            data = json.loads(barcode_data)

            land = data['land']
            variety = data['variety']
            measurement_id = data['measurement_id']

            engine = create_engine('mysql+pymysql://root:123456@localhost/local_db')
            Session = sessionmaker(bind=engine)
            session = Session()

            self.insert_measurement(session, land, variety, measurement_id)
            self.close_camera()

            self.qr_verified = True
            self.load_gps_page(land, variety)

        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Invalid QR code data: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error verifying QR code: {e}")
        finally:
            session.close()

    def load_gps_page(self, land, variety):
        self.master.current_page.destroy()
        self.master.current_page = LoadGPS(self.master, land, variety)
        self.master.current_page.pack(fill=tk.BOTH, expand=True)

    def insert_measurement(self, session, land, variety, measurement_id):
        try:
            sql = text("INSERT INTO measurements (measurement_id, land, variety) VALUES (:measurement_id, :land, :variety) ON DUPLICATE KEY UPDATE variety=:variety")
            session.execute(sql, {"measurement_id": measurement_id, "land": land, "variety": variety})
            session.commit()
        except IntegrityError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    welcome_page = WelcomePage(root)
    CheckQRCode(root, welcome_page).pack(fill=tk.BOTH, expand=True)
    root.protocol("WM_DELETE_WINDOW", lambda: root.quit())  # Ensure the camera is closed on exit
    root.mainloop()

import qrcode
import json
import os
from cryptography.fernet import Fernet

# Fungsi untuk mengambil data JSON dari sumber dinamis
def get_dynamic_json_data():
    data = {
        "lahan": {
            "id_lahan": int(input("Masukkan ID Lahan: ")),
            "nama_lahan": input("Masukkan Nama Lahan: ")
        },
        "varietas": {
            "id_varietas": int(input("Masukkan ID Varietas: ")),
            "nama_varietas": input("Masukkan Nama Varietas: ")
        }
    }
    return data

# Load the encryption key from the file
with open('secret.key', 'rb') as key_file:
    key = key_file.read()

cipher = Fernet(key)

# Ambil data JSON dinamis
data = get_dynamic_json_data()

# Convert JSON data to string and then encrypt it
json_data = json.dumps(data)
encrypted_data = cipher.encrypt(json_data.encode())

# Generate QR code
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
qr.add_data(encrypted_data.decode())
qr.make(fit=True)

# Function to generate unique filename
def get_unique_filename(base_filename):
    if not os.path.exists(base_filename):
        return base_filename
    else:
        base, ext = os.path.splitext(base_filename)
        counter = 1
        new_filename = f"{base}_{counter}{ext}"
        while os.path.exists(new_filename):
            counter += 1
            new_filename = f"{base}_{counter}{ext}"
        return new_filename

# Save QR code image
base_filename = 'encrypted_qr.png'
filename = get_unique_filename(base_filename)
img = qr.make_image(fill='black', back_color='white')
img.save(filename)

print(f"QR Code generated and saved as '{filename}'.")

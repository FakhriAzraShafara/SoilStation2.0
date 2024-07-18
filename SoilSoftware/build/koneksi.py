import socket
import subprocess

def check_internet_connection(host="103.155.246.91", port=22, timeout=3):
    """
    Fungsi ini memeriksa koneksi internet dengan mencoba membuat koneksi ke host dan port server iotanic.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        print("Koneksi internet aktif")
        return True
        subprocess.run(['python3', 'scan_qr.py'])
        sys.exit()
    except socket.error as ex:
        print("Tidak ada koneksi internet:", ex)
        return False
        subprocess.run(['python3', 'wifi_manager.py'])

if __name__ == "__main__":
    check_internet_connection()

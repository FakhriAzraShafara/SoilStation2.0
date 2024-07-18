import serial
import time
import subprocess
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError
from adafruit import adafruit_gps

# Definisikan model tabel GPS
Base = declarative_base()

class GPSData(Base):
    __tablename__ = 'gps'
    id_gps = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Float)
    longitude = Column(Float)

# Fungsi untuk memasukkan data GPS ke dalam database
def insert_gps_data(session, latitude, longitude):
    try:
        new_gps = GPSData(latitude=latitude, longitude=longitude)
        session.add(new_gps)
        session.commit()
        print("Data GPS berhasil dimasukkan ke database")
    except IntegrityError:
        session.rollback()
        print("Data GPS sudah ada di database")

# Buat engine dan sesi SQLAlchemy
DATABASE_URL = "mysql+pymysql://root:123456@localhost/local_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Ciptakan tabel jika belum ada
Base.metadata.create_all(engine)

def run_gps_acquisition():
    results = []
    last_latitude = None
    last_longitude = None
    session = Session()

    try:
        with serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=10) as uart:
            gps = adafruit_gps.GPS(uart, debug=False)  # Membuat instance GPS dari adafruit_gps
            gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
            gps.send_command(b"PMTK220,1000")
            
            last_print = time.monotonic()
            counter = 0
            
            while counter < 10:
                gps.update()
                current = time.monotonic()
                if current - last_print >= 1.0:
                    last_print = current
                    counter += 1
                    
                    if not gps.has_fix:
                        results.append("Menunggu fix...")
                        continue
                    
                    result = [
                        "Fix timestamp:        {}/{}/{} {:02}:{:02}:{:02}".format(
                            gps.timestamp_utc.tm_mon,
                            gps.timestamp_utc.tm_mday,
                            gps.timestamp_utc.tm_year,
                            gps.timestamp_utc.tm_hour,
                            gps.timestamp_utc.tm_min,
                            gps.timestamp_utc.tm_sec,
                        ),
                        "Latitude:             {0:.6f} derajat".format(gps.latitude),
                        "Longitude:            {0:.6f} derajat".format(gps.longitude),
                    ]

                    if gps.satellites is not None:
                        result.append("Jumlah satelit: {}".format(gps.satellites))
                    if gps.altitude_m is not None:
                        result.append("Altitude:             {} meter".format(gps.altitude_m))
                    
                    results.append("\n".join(result))
                    
                    # Simpan data GPS terakhir
                    last_latitude = gps.latitude
                    last_longitude = gps.longitude

                    if last_latitude is not None and last_longitude is not None:
                        insert_gps_data(session, last_latitude, last_longitude)
                        return True  # Data berhasil didapatkan, hentikan eksekusi
    except serial.SerialException as e:
        print('Tidak dapat membuka port serial:', e)
        results.append(f'Tidak dapat membuka port serial: {e}')
    except Exception as e:
        print('Terjadi kesalahan:', e)
        results.append(f'Terjadi kesalahan: {e}')
    finally:
        session.close()
        
        # Cetak semua hasil
        for i, result in enumerate(results):
            print(f"Iterasi {i + 1}:")
            print(result)
            print("-" * 20)
    
    return False  # Data tidak berhasil didapatkan

if __name__ == "__main__":
    while True:
        try:
            data_acquired = run_gps_acquisition()
            if data_acquired:
                break
        except Exception as e:
            print("Terjadi kesalahan, menjalankan tunggu_gps.py")
            continue  # Mulai ulang loop

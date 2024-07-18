import serial
import time
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError
from adafruit import adafruit_gps

# Definisikan model tabel GPS
Base = declarative_base()

class GPSData(Base):
    __tablename__ = 'gps'
    id_gps = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

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

def run_gps_acquisition(max_retries=1):
    session = Session()
    retries = 0

    while retries < max_retries:
        try:
            with serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=10) as uart:
                gps = adafruit_gps.GPS(uart, debug=False)
                gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
                gps.send_command(b"PMTK220,1000")

                start_time = time.monotonic()
                while time.monotonic() - start_time < 60:
                    gps.update()
                    if not gps.has_fix:
                        print("Menunggu fix...")
                        time.sleep(1)
                        continue

                    latitude = gps.latitude
                    longitude = gps.longitude

                    if latitude is not None and longitude is not None:
                        insert_gps_data(session, latitude, longitude)
                        return True  # Data berhasil didapatkan

        except serial.SerialException as e:
            print('Tidak dapat membuka port serial:', e)
        except Exception as e:
            print('Terjadi kesalahan:', e)

        retries += 1
        print(f"Percobaan {retries} gagal, mencoba lagi...")

    # Jika tidak mendapatkan data GPS setelah max_retries
    insert_gps_data(session, None, None)
    print("Data GPS tidak berhasil didapatkan setelah beberapa kali percobaan")
    session.close()
    return False  # Data tidak berhasil didapatkan

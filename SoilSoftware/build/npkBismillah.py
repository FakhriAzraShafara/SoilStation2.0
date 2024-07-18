import serial
import time
import logging
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Serial port initialization
uart0 = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

# Command definitions
commands = {
    'ph': bytes.fromhex('01 03 00 06 00 01 64 0b'),
    'nitrogen': bytes.fromhex('01 03 00 1e 00 01 e4 0c'),
    'phosphorus': bytes.fromhex('01 03 00 1f 00 01 b5 cc'),
    'potassium': bytes.fromhex('01 03 00 20 00 01 85 c0')
}

# SQLAlchemy setup
Base = declarative_base()

class NPK(Base):
    __tablename__ = 'npk'

    id_npk = Column(Integer, primary_key=True, autoincrement=True)
    natrium = Column(Float)
    fosfor = Column(Float)
    kalium = Column(Float)
    ph = Column(Float)

engine = create_engine('mysql+pymysql://root:123456@localhost/local_db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Function to send command and receive data
def get_sensor_value(command):
    uart0.write(command)
    rx_data = uart0.read(7)
    if len(rx_data) == 7:
        sensor_value = int.from_bytes(rx_data[3:5], 'big')
        return sensor_value
    else:
        return None

# Function to collect 100 readings and calculate average
def collect_and_average():
    ph_values = []
    nitrogen_values = []
    phosphorus_values = []
    potassium_values = []

    for _ in range(100):
        # Receive data
        pH = get_sensor_value(commands['ph'])
        if pH is not None:
            pH /= 100.0
            ph_values.append(pH)
        
        N = get_sensor_value(commands['nitrogen'])
        if N is not None:
            nitrogen_values.append(N)
        
        P = get_sensor_value(commands['phosphorus'])
        if P is not None:
            phosphorus_values.append(P)
        
        K = get_sensor_value(commands['potassium'])
        if K is not None:
            potassium_values.append(K)

    # Calculate averages
    avg_pH = round(sum(ph_values) / len(ph_values), 2) if ph_values else None
    avg_N = round(sum(nitrogen_values) / len(nitrogen_values), 2) if nitrogen_values else None
    avg_P = round(sum(phosphorus_values) / len(phosphorus_values), 2) if phosphorus_values else None
    avg_K = round(sum(potassium_values) / len(potassium_values), 2) if potassium_values else None

    logging.info("Average pH: {}".format(avg_pH))
    logging.info("Average Nitrogen: {}".format(avg_N))
    logging.info("Average Phosphorus: {}".format(avg_P))
    logging.info("Average Potassium: {}".format(avg_K))

    # Insert data into database
    if None not in (avg_N, avg_P, avg_K, avg_pH):
        insert_data(avg_N, avg_P, avg_K, avg_pH)

def insert_data(nitrogen, phosphorus, potassium, pH):
    new_data = NPK(natrium=nitrogen, fosfor=phosphorus, kalium=potassium, ph=pH)
    session.add(new_data)
    try:
        session.commit()
        logging.info("Data inserted into database")
    except Exception as e:
        logging.error("Failed to insert data: %s", str(e))
        session.rollback()

if __name__ == "__main__":
    logging.info('""""""""""""""""""""""""""""""')
    logging.info('proses pengukuran...')
    logging.info('==============================')
    try:
        collect_and_average()
    except Exception as e:
        logging.error("An error occurred during measurement: %s", str(e))
    finally:
        uart0.close()
        session.close()

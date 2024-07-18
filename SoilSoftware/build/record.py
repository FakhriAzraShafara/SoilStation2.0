from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# Setup engine and session
engine = create_engine('mysql+pymysql://root:123456@localhost/local_db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define model for record
class Record(Base):
    __tablename__ = 'record'

    id_record = Column(Integer, primary_key=True)
    id_gps = Column(Integer, ForeignKey('gps.id_gps'), nullable=True)
    id_npk = Column(Integer, ForeignKey('npk.id_npk'), nullable=True)
    time_records = Column(DateTime, default=datetime.now)
    measurement_id = Column(String(50), ForeignKey('measurements.measurement_id'), nullable=False)

# Define models for other tables (measurement, lahan, gps, npk)
class Measurement(Base):
    __tablename__ = 'measurements'

    measurement_id = Column(String(50), primary_key=True)
    land = Column(String(50))
    variety = Column(String(50))

class Lahan(Base):
    __tablename__ = 'lahan'

    id_lahan = Column(String(15), primary_key=True)
    nama_lahan = Column(String(255))

class GPS(Base):
    __tablename__ = 'gps'

    id_gps = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)

class NPK(Base):
    __tablename__ = 'npk'

    id_npk = Column(Integer, primary_key=True)
    natrium = Column(Float)
    fosfor = Column(Float)
    kalium = Column(Float)
    ph = Column(Float)

# Create tables if not exist
Base.metadata.create_all(engine)

# Query latest data from tables
latest_gps = session.query(GPS).order_by(GPS.id_gps.desc()).first()
latest_npk = session.query(NPK).order_by(NPK.id_npk.desc()).first()
latest_measurement = session.query(Measurement).order_by(Measurement.measurement_id.desc()).first()

# Check if id_gps and id_npk combination already exists in record table
existing_record = session.query(Record).filter_by(
    id_gps=latest_gps.id_gps if latest_gps else None, 
    id_npk=latest_npk.id_npk if latest_npk else None
).first()

# Insert latest data into record table if combination does not exist
if not existing_record:
    new_record = Record(
        id_gps=latest_gps.id_gps if latest_gps else None,
        id_npk=latest_npk.id_npk if latest_npk else None,
        time_records=datetime.now(),
        measurement_id=latest_measurement.measurement_id if latest_measurement else None
    )

    session.add(new_record)
    session.commit()
    print("Data successfully inserted into record table.")
else:
    print(f"Combination of id_gps ({latest_gps.id_gps}) and id_npk ({latest_npk.id_npk}) already exists in record table. Skipping insertion.")

# Close session
session.close()

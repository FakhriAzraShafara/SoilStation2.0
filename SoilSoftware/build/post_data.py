import pandas as pd
from sqlalchemy import create_engine, text
import paho.mqtt.client as mqtt
import json

# Buat engine SQLAlchemy untuk koneksi ke MariaDB
engine = create_engine('mysql+pymysql://root:123456@localhost/local_db', echo=True)  # Aktifkan logging SQL dengan echo=True

# Fungsi untuk mengambil data dari database menggunakan SQLAlchemy
def fetch_records():
    try:
        # Query SQL untuk mengambil data dari tabel record dengan join ke tabel gps dan npk
        sql = """
        SELECT 
            r.id_record,
            g.latitude,
            g.longitude,
            n.natrium,
            n.fosfor,
            n.kalium,
            n.ph,
            r.time_records,
            r.measurement_id
        FROM record r
        LEFT JOIN gps g ON r.id_gps = g.id_gps
        LEFT JOIN npk n ON r.id_npk = n.id_npk;
        """
        with engine.connect() as conn:
            records_df = pd.read_sql(sql, con=conn)
    except Exception as e:
        print(f"Error querying database: {e}")
        records_df = pd.DataFrame()

    return records_df

# Fungsi untuk mengubah kolom Timestamp menjadi string format ISO
def convert_timestamp_to_str(ts):
    if isinstance(ts, pd.Timestamp):
        return ts.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return str(ts)

# Fungsi untuk mengirim data menggunakan MQTT
def send_records(records_df):
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set("user1", "user123")  # Tambahkan autentikasi user dan password
    try:
        mqtt_client.connect("103.155.246.91", 18831, 60)  # Tambahkan timeout 60 detik
        mqtt_client.loop_start()

        # Mengubah DataFrame ke dalam bentuk list of dictionaries
        records_list = records_df.to_dict('records')

        for record in records_list:
            # Mengubah Timestamp menjadi string format ISO
            record['time_records'] = convert_timestamp_to_str(record['time_records'])
            
            # Pastikan latitude dan longitude nullable
            if pd.notnull(record['latitude']):
                record['latitude'] = f"{float(record['latitude']):.6f}"
            if pd.notnull(record['longitude']):
                record['longitude'] = f"{float(record['longitude']):.6f}"
            
            # Publish data ke topik 'record/data'
            mqtt_client.publish("record/data", json.dumps(record))
            print(record)

        mqtt_client.loop_stop()
        mqtt_client.disconnect()
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")

# Fungsi untuk mengosongkan tabel menggunakan nama tabel sebagai parameter
def clear_table(table_name):
    try:
        with engine.connect() as conn:
            conn.execute(text(f"DELETE FROM {table_name}"))
            conn.commit()  # Commit setelah setiap penghapusan
            print(f'Success Clearing TABLE {table_name}')
    except Exception as e:
        print(f"Error clearing table {table_name}: {e}")

# Main program
if __name__ == "__main__":
    # Ambil data dari database menggunakan SQLAlchemy dan pandas
    records_df = fetch_records()

    # Kirim data menggunakan MQTT jika ada data yang berhasil diambil
    if not records_df.empty:
        send_records(records_df)
        print(f"Successfully sent {len(records_df)} records.")
        # Hapus data setelah berhasil dikirim
        clear_table('record')
        # Hapus data dari tabel gps dan npk setelah tabel record dihapus
        clear_table('gps')
        clear_table('npk')
    else:
        print("No record found or error occurred.")

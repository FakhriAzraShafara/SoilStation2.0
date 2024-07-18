import pandas as pd
from sqlalchemy import create_engine
from geopy.distance import geodesic

# Membuat koneksi ke database MySQL
engine = create_engine('mysql+pymysql://root:123456@localhost/local_db')

# Fungsi untuk menentukan kota berdasarkan koordinat GPS
def determine_city(latitude, longitude, df_wilayah, radius_km=10):
    current_location = (latitude, longitude)
    
    for index, row in df_wilayah.iterrows():
        city_location = (row['latitude'], row['longitude'])
        distance = geodesic(current_location, city_location).kilometers
        if distance <= radius_km:
            return row['name']
    
    return None

# Fungsi utama untuk menemukan kota berdasarkan koordinat terakhir
def find_city_by_coordinates():
    # Memuat data wilayah ke dalam DataFrame
    query_wilayah = "SELECT name, latitude, longitude FROM wilayah"
    df_wilayah = pd.read_sql(query_wilayah, engine)
    
    # Mengambil data latitude dan longitude terakhir dari tabel gps
    query_gps = "SELECT latitude, longitude FROM gps ORDER BY id_gps DESC LIMIT 1"
    df_gps = pd.read_sql(query_gps, engine)
    
    if df_gps.empty:
        return "lokasi tidak tercatat"
    
    latitude = df_gps['latitude'].iloc[0]
    longitude = df_gps['longitude'].iloc[0]
    
    city = determine_city(latitude, longitude, df_wilayah)
    if city:
        return f"{city}"
    else:
        return "Lokasi tidak tercatat"

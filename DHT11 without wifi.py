import machine
import dht
import time

# Inisialisasi sensor DHT11 (ubah pin)
sensor = dht.DHT11(machine.Pin(5))

while True:
    try:
        sensor.measure()  # Mengambil data dari sensor
        suhu = sensor.temperature()  # Ambil suhu dalam Celcius
        kelembaban = sensor.humidity()  # Ambil kelembaban dalam %

        print("Suhu: {}°C  Kelembaban: {}%".format(suhu, kelembaban))
    
    except OSError as e:
        print("Gagal membaca sensor!", e)
    
    time.sleep(2) 

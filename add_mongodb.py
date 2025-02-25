import machine
import dht
import time
import network
import ubinascii
import ujson
import urequests
from umqtt.simple import MQTTClient
from ssd1306 import SSD1306_I2C

# Konfigurasi WiFi
SSID = "LAB 2"
PASSWORD = "bersahaja"

# Konfigurasi Ubidots
TOKEN = "BBUS-Iv0eA6qUT5xwkwvVzKMdmFI8UPSF8C"
DEVICE_ID = "67b87284661d433b2383ce36"
LABEL = "esp32"
BROKER = "industrial.api.ubidots.com"
TOPIC = f"/v1.6/devices/{LABEL}"

# Konfigurasi MongoDB
MONGODB_URL = "http://192.168.0.115:6000/data"

# Koneksi ke WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        pass
    print("WiFi Connected!", wlan.ifconfig())

# Koneksi ke MQTT Ubidots
def connect_mqtt():
    client_id = ubinascii.hexlify(machine.unique_id()).decode()
    client = MQTTClient(client_id, BROKER, user=TOKEN, password="", port=1883, keepalive=60)
    client.connect()
    print("Connected to Ubidots MQTT Broker")
    return client

# Fungsi mengirim data ke MongoDB melalui HTTP
def send_to_mongodb(value):
    payload = ujson.dumps({"temperature": value})
    headers = {'Content-Type': 'application/json'}
    response = urequests.post(MONGODB_URL, data=payload, headers=headers)
    response.close()

# Inisialisasi sensor DHT11 di pin D5
sensor = dht.DHT11(machine.Pin(5))

# Inisialisasi layar OLED (SSD1306) di GPIO 21 (SDA) dan 22 (SCL)
i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21))
display = SSD1306_I2C(128, 64, i2c)

def update_display(suhu, kelembaban):
    display.fill(0)
    display.text("ESP32 Sensor", 0, 0)
    display.text(f"Temp: {suhu}C", 0, 20)
    display.text(f"Hum: {kelembaban}%", 0, 40)
    display.show()

connect_wifi()
client = connect_mqtt()

while True:
    try:
        sensor.measure()
        suhu = sensor.temperature()
        kelembaban = sensor.humidity()

        print(f"Suhu: {suhu}°C | Kelembaban: {kelembaban}%")
        
        payload = f'{{"temperature": {suhu}, "humidity": {kelembaban}}}'
        client.publish(TOPIC, payload)
        print("Data sent to Ubidots")
        
        update_display(suhu, kelembaban)
    
    except OSError as e:
        print("Gagal membaca sensor!", e)
    
    time.sleep(1)


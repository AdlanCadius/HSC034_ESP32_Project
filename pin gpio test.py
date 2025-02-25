import machine
import time

pin = machine.Pin(5, machine.Pin.IN)  # Atur GPIO15 sebagai input

while True:
    pin_status = pin.value()  # Baca status pin
    print("Status Pin D4:", pin_status)
    time.sleep(19999)  # Tunggu 1 detik sebelum membaca lagi

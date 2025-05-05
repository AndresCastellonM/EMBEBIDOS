import serial
import time

# Configurar UART en Raspberry Pi
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Esperar a que la conexión se estabilice

while True:
    ser.write(b'Hola desde Raspberry\n')  # Enviar mensaje a Arduino
    time.sleep(1)

    if ser.in_waiting > 0:  # Si hay datos disponibles
        received_data = ser.readline().decode('utf-8').strip()
        print("Arduino dice:", received_data)

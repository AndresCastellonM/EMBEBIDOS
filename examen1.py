import RPi.GPIO as GPIO
import time
import serial
import smtplib
from datetime import datetime

# Configuración de pines
BUTTON_PIN = 17  # GPIO del botón
TRIG_PIN = 23    # GPIO del trigger del sensor ultrasónico
ECHO_PIN = 24    # GPIO del echo del sensor ultrasónico
TRIG2 = 23
ECHO2 = 24

# Variables globales
flag_led = 0
flag_temp = None
temp = 0
pwmLed1 = 0
pwmLed2 = 0
led1 = 0
led2 = 0
pwmLed1_prev = 0
pwmLed2_prev = 0
estado_leds = 0
ALARM_STATE = "OFF"
timestamp = None
tiempo_activado = 0
metodo = ""

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)

# Configuración de UART
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
ser.flush()

def read_controller(): #leer archivo con variables
    global temp, pwmLed1, pwmLed2
    try:
        with open("controller.txt", "r") as file:
            for line in file:
                if "Temp(C)=" in line:
                    temp = float(line.strip().split("=")[1])
                elif "led1(%)=" in line:
                    pwmLed1 = float(line.strip().split("=")[1])
                elif "led2(%)=" in line:
                    pwmLed2 = float(line.strip().split("=")[1])
    except Exception as e:
        print("Error al leer el archivo:", e)

def validate_values():
    global pwmLed1, pwmLed2, changes1, pwmLed1, pwmLed2
    try:
        pwmLed1 = max(1, min(100, int(pwmLed1)))
        pwmLed2 = max(1, min(100, int(pwmLed2)))
        if pwmLed1 != pwmLed1_prev or pwmLed2 != pwmLed2_prev:
            flag_led = 1
            pwmLed1_prev, pwmLed2_prev = pwmLed1, pwmLed2
    except ValueError:
        print("Valores inválidos en el archivo")

def measure_distance():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        end_time = time.time()
    duration = end_time - start_time
    return (duration * 34300) / 2  # Distancia en cm

def check_temperature():
    global flag_temp
    if temp > 20:
        message = "cooler"
    elif temp < 2:
        message = "heater"
    else:
        message="nada"
    if message != flag:
        ser.write((message + "\n").encode())
        flag_temp = message


def measure_distance2(): # Función para medir distancia con promedio de 5 lecturas
    distances = []
    for _ in range(5):
        GPIO.output(TRIG2, True)
        time.sleep(0.00001)
        GPIO.output(TRIG2, False)
        
        while GPIO.input(ECHO2) == 0:
            start_time = time.time()
        while GPIO.input(ECHO2) == 1:
            end_time = time.time()
        
        elapsed_time = end_time - start_time
        distance = (elapsed_time * 34300) / 2
        distances.append(distance)
        time.sleep(0.05)
    return sum(distances) / len(distances)

def button_callback(channel):
    global estado_leds, changes1, led1, led2
    estado = (estado + 1) % 4
    if estado == 0:
        led1, led2 = 0, 0
    elif estado == 1:
        led1, led2 = 1, 0
    elif estado == 2:
        led1, led2 = 0, 1
    elif estado == 3:
        led1, led2 = 1, 1
    changes1 = 1

# Función para activar/desactivar la alarma
def control_alarm():
    global ALARM_STATE, timestamp, tiempo_activado, metodo
    
    distance = measure_distance2()
    if distance < 7 and ALARM_STATE == "OFF":
        timestamp = datetime.now()
        ALARM_STATE = "ON"
        with open("controller.txt", "r+") as file:
            content = file.read()
            content = content.replace("ALARM=OFF", "ALARM=ON")
            file.seek(0)
            file.write(content)
            file.truncate()
        ser.write(b"alarm\n")
    
    elif distance >= 7 and ALARM_STATE == "ON":
        tiempo_activado = (datetime.now() - timestamp).total_seconds()
        metodo = "el objeto fue alejado"
        detener_alarma()
    
    with open("controller.txt", "r") as file:
        content = file.read()
        if "ALARM=OFF" in content and ALARM_STATE == "ON":
            tiempo_activado = (datetime.now() - timestamp).total_seconds()
            metodo = "SSH, desactivacion manual"
            detener_alarma()

# Función para detener la alarma y enviar email
def detener_alarma():
    global ALARM_STATE
    ALARM_STATE = "OFF"
    ser.write(b"alarmoff\n")
    with open("controller.txt", "r+") as file:
        content = file.read()
        content = content.replace("ALARM=ON", "ALARM=OFF")
        file.seek(0)
        file.write(content)
        file.truncate()
    #enviar_email()
    print("Se envio el email!")

# Función para enviar email
def enviar_email():
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("sender_email_id", "sender_email_id_password")
    
    message = f"La alarma fue activada a las {timestamp} por un tiempo de {tiempo_activado} segundos y fue apagada por {metodo}."
    s.sendmail("sender_email_id", "receiver_email_id", message)
    s.quit()


#main void
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)
# Bucle principal

while True:
    read_controller()
    validate_values()
    control_alarm()

    distance = measure_distance()
    if distance < 7:
        ser.write("garaje\n".encode())

    check_temperature()

    if changes1:
        ser.write(f"{led1},{led2},{pwmLed1},{pwmLed2}\n".encode())
        changes1 = 0
    
    time.sleep(1)



import random
import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    import unittest.mock as mock
    GPIO = mock.MagicMock()

fan = 14
heater = 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(fan, GPIO.OUT)
GPIO.setup(heater, GPIO.OUT)

while True:
    temp = random.randint(0, 40)  
    print(f"Temperatura: {temp}°C")

    if temp < 12:
        GPIO.output(heater, GPIO.HIGH)  
        GPIO.output(fan, GPIO.LOW)  
    elif temp > 20:
        GPIO.output(fan, GPIO.HIGH)
        GPIO.output(heater, GPIO.LOW)  
    else:
        GPIO.output(heater, GPIO.LOW)
        GPIO.output(fan, GPIO.LOW)

    time.sleep(5)


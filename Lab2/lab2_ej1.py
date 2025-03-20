import time

# Intentar importar RPi.GPIO, si falla, usar un mock
try:
    import RPi.GPIO as GPIO
except ImportError:
    import unittest.mock as mock
    GPIO = mock.MagicMock()

led1 = 2 #pin 3
led2 = 3 #pin5
button1 = 27 #pin 13
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)


#ejercicio 1
c = 1;
while True:
    while c == 1:
        GPIO.output(led1, GPIO.HIGH)
        GPIO.output(led2, GPIO.LOW)
        time.sleep(1)
        GPIO.output(led1, GPIO.LOW)
        GPIO.output(led2, GPIO.HIGH)
        time.sleep(1)
        if GPIO.input(button1) == GPIO.LOW:
            c += 1
    while c == 2:
        GPIO.output(led1, GPIO.HIGH)
        GPIO.output(led2, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(led1, GPIO.LOW)
        GPIO.output(led2, GPIO.LOW)
        time.sleep(2)
        if GPIO.input(button1) == GPIO.LOW:
            c += 1
    while c == 3:
        GPIO.output(led1, GPIO.HIGH)
        GPIO.output(led2, GPIO.HIGH)
        if GPIO.input(button1) == GPIO.LOW:
            c += 1
    while c == 4:
        GPIO.output(led1, GPIO.LOW)
        GPIO.output(led2, GPIO.LOW)
        if GPIO.input(button1) == GPIO.LOW:
            c = 1
try:
    import RPi.GPIO as GPIO
except ImportError:
    import unittest.mock as mock
    GPIO = mock.MagicMock()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
led1, led2, led3, led4 = 2, 3, 4, 17
button1, button2 = 27, 22
GPIO.setup(led1, GPIO.OUT); GPIO.setup(led2, GPIO.OUT); GPIO.setup(led3, GPIO.OUT); GPIO.setup(led4, GPIO.OUT);
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class Contador:
    def __init__(self, bits=4):
        self.valor = 0
        self.bits = bits
        self.max_val = 2**bits - 1

    def add(self, cant):
        self.valor += cant
        if self.valor < 0:
            self.valor = 0
        if self.valor > self.max_val:
            self.valor = self.valor % (self.max_val + 1)

    def show(self):
        print(f"Decimal: \t {self.valor}")
        print(f"Binario: \t {bin(self.valor)}")
        print(f"Hexadecimal: \t {hex(self.valor)}")

    def ledState(self, led_pin, state):
        GPIO.setmode(GPIO.BCM)  # Asegurar que el modo está definido
        GPIO.setup(led_pin, GPIO.OUT)
        if state == '1':
            GPIO.output(led_pin, GPIO.HIGH)
        else:
            GPIO.output(led_pin, GPIO.LOW)

    

cont1 = Contador
leds_pins = [led1, led2, led3, led4]
while True:
    while True:
        if GPIO.input(button1) == GPIO.LOW:
            cont1.add(1)
            break
        if GPIO.input(button2) == GPIO.LOW:
            cont1.add(-1)
            break
    binario = str(bin(cont1.valor))
    binario = binario[2:]
    for i, led in zip(range(len(leds_pins)), leds_pins):
        try:
            val = binario[-i-1]
        except IndexError:
            val = 0
        finally:
            cont1.ledState(led, val)
        


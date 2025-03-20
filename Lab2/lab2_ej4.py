import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    import unittest.mock as mock
    GPIO = mock.MagicMock()

# Definición de pines
led1, led2, led3, led4 = 2, 3, 4, 17
button1, button2 = 27, 22

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup([led1, led2, led3, led4], GPIO.OUT)
GPIO.setup([button1, button2], GPIO.IN, pull_up_down=GPIO.PULLUP)  # Activar pull-up

# Variables
led_num = 0
freq_blink = 1
leds_pins = [led1, led2, led3, led4]

def turn_off():
    """Apaga todos los LEDs"""
    for led in leds_pins:
        GPIO.output(led, GPIO.LOW)

def blink_led(led_num, freq_blink):
    """Hace parpadear un LED específico con la frecuencia dada"""
    GPIO.output(leds_pins[led_num], GPIO.HIGH)
    time.sleep(freq_blink)
    GPIO.output(leds_pins[led_num], GPIO.LOW)
    time.sleep(freq_blink)

try:
    while True:
        while GPIO.input(button1) == GPIO.HIGH:  # Espera a que se presione el botón 1
            blink_led(led_num, freq_blink)
            if GPIO.input(button2) == GPIO.LOW:  # Si el botón 2 se presiona, aumenta la frecuencia
                freq_blink += 1
                time.sleep(0.2)  # Pequeña pausa para evitar rebotes

        led_num = (led_num + 1) % 4  # Cambia al siguiente LED en la lista
        turn_off()
        freq_blink = 1  # Reinicia la frecuencia

except KeyboardInterrupt:
    print("Saliendo...")
    GPIO.cleanup()  # Restablece los pines GPIO al salir

#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"

// Definir pines de LEDs (PORTN y PORTF)
#define LED1 GPIO_PIN_1  // PN1
#define LED2 GPIO_PIN_0  // PN0
#define LED3 GPIO_PIN_4  // PF4
#define LED4 GPIO_PIN_0  // PF0

// Definir pines de botones (PORTJ)
#define BUTTON1 GPIO_PIN_0  // PJ0
#define BUTTON2 GPIO_PIN_1  // PJ1

void delay(void)
{
    SysCtlDelay(120000000 / (6));  // Aproximadamente 2 segundos
}

void led_sequence_ascending(void)
{
    // Encender LEDs uno por uno en orden ascendente
    GPIOPinWrite(GPIO_PORTN_BASE, LED1, LED1);
    delay();
    GPIOPinWrite(GPIO_PORTN_BASE, LED2, LED2);
    delay();
    GPIOPinWrite(GPIO_PORTF_BASE, LED3, LED3);
    delay();
    GPIOPinWrite(GPIO_PORTF_BASE, LED4, LED4);
    delay();
}

void led_sequence_descending(void)
{
    // Apagar LEDs uno por uno en orden descendente
    GPIOPinWrite(GPIO_PORTF_BASE, LED4, 0);
    delay();
    GPIOPinWrite(GPIO_PORTF_BASE, LED3, 0);
    delay();
    GPIOPinWrite(GPIO_PORTN_BASE, LED2, 0);
    delay();
    GPIOPinWrite(GPIO_PORTN_BASE, LED1, 0);
    delay();
}

int main(void)
{
    // Habilitar los puertos de los LEDs y los botones
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);

    // Esperar hasta que los puertos estén listos
    while (!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION)) {}
    while (!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF)) {}
    while (!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOJ)) {}

    // Configurar pines de LEDs como salida
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, LED1 | LED2);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, LED3 | LED4);

    // Configurar pines de botones como entrada con Pull-Up
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, BUTTON1 | BUTTON2);
    GPIOPadConfigSet(GPIO_PORTJ_BASE, BUTTON1 | BUTTON2, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);

    while (1)
    {
        if (GPIOPinRead(GPIO_PORTJ_BASE, BUTTON1) == 0)  // Botón 1 presionado
        {
            led_sequence_ascending();
        }
        if (GPIOPinRead(GPIO_PORTJ_BASE, BUTTON2) == 0)  // Botón 2 presionado
        {
            led_sequence_descending();
        }
    }
}

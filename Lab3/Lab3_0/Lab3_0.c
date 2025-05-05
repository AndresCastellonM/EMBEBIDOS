//*******************************************************************
// LIBRERIAS
//*******************************************************************

#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/debug.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"
//*******************************************************************
// La rutina de error que se llama si la biblioteca del controlador encuentra un error.
//*******************************************************************
#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
    while(1);
}
#endif
//*******************************************************************
// Función principal
//*******************************************************************

int main(void)
{
    volatile uint32_t ui32Loop;
    bool buttonPressed = false;  // Variable para detectar si el botón fue presionado
    bool ledsActive = false;     // Variable para controlar el estado de los LEDs

    // Configura el reloj del sistema a 120 MHz
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480), 120000000);

    // Habilita los periféricos GPIO N, F y J
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);  // Para los LEDs en el puerto N
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);  // Para los LEDs en el puerto F
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);  // Para el botón en el puerto J

    // Espera a que los periféricos estén listos
    while (!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION)) {}
    while (!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF)) {}
    while (!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOJ)) {}

    // Configura los pines de los LEDs como salidas
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1);  // LEDs en PN0 y PN1
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4);  // LEDs en PF0 y PF4

    // Configura el pin del botón como entrada con resistencia pull-up
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_0);  // Botón en PJ0
    GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_0, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);

//BUCLE INFINITO ****************************************************
    while (1) {
        // Verifica si el botón fue presionado
        if (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0) { // Si el botón está presionado (0 = activo bajo)
            if (!buttonPressed) { // Evita múltiples detecciones mientras el botón está presionado
                buttonPressed = true;
                ledsActive = !ledsActive;  // Cambia el estado de los LEDs (activo/inactivo)
            }
        }
        else {
            buttonPressed = false;  // Reinicia la detección del botón
        }

        // Si los LEDs están activos
        if (ledsActive) {
            // Enciende los primeros dos LEDs (PN0 y PN1)
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1, GPIO_PIN_0 | GPIO_PIN_1);

            // Espera 2 segundos (ajusta el valor del bucle para un retardo preciso)
            for (ui32Loop = 0; ui32Loop < 20000000; ui32Loop++) {}

            // Enciende los otros dos LEDs (PF0 y PF4)
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4, GPIO_PIN_0 | GPIO_PIN_4);

            
            // Espera 2 segundos
            for (ui32Loop = 0; ui32Loop < 20000000; ui32Loop++) {}
        }
        else {
            // Apaga todos los LEDs
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1, 0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4, 0);
        }
    }
}

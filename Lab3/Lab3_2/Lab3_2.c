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

    // Configura el reloj del sistema a 120 MHz
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480), 120000000);

    // Habilita los periféricos GPIO N, F y J
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);  // Para los LEDs en el puerto N
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);  // Para los LEDs en el puerto F

    // Espera a que los periféricos estén listos
    while (!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION)) {}
    while (!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF)) {}

    // Configura los pines de los LEDs como salidas
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1);  // LEDs en PN0 y PN1
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4);  // LEDs en PF0 y PF4


//BUCLE INFINITO ****************************************************
    while (1) {
         // Enciende los LEDs
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);
        SysCtlDelay(120000000 / 3);    
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
        SysCtlDelay(120000000 / 3);    
         // Apaga los LEDs
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0);
        SysCtlDelay(120000000 / 3);    
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0);
        SysCtlDelay(120000000 / 3);    
    }
}

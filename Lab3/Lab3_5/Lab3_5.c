#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/debug.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"

//Esta función se llama si ocurre un error en modo depuración (DEBUG). Entra en un bucle infinito para detener la ejecución.
#ifdef DEBUG
void __error__(char *pcFilename, uint32_t ui32Line)
{
    while(1);
}
#endif
void delay(void)
{
    SysCtlDelay(120000000/(22/2)); // Aproximadamente 2 segundos
}
void state1(void){
    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1); 
    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0); 
    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4); 
    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);

}

void state2(void){
    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0); 
    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0); 
    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0); 
    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0);
}

void state3(void){
    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1); 
    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0); 
    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4); 
    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0);
}

void state4(void){
    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1); 
    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0); 
    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0); 
    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0);
}


int main(void)
{
    //volatile uint32_t ui32Loop;

    // Habilitar los puertos GPIO para los LEDs y los interruptores
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ); // Para los interruptores en PJ0-PJ1

    // Asegurarse de que los puertos GPIO están listos
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION)) {}
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF)) {}
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOJ)) {}

    // Configurar los pines de los LEDs como salida
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4);

    // Configurar los pines de los interruptores como entrada
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_0 | GPIO_PIN_1);

    // Habilitar las resistencias de Pull-Up para los interruptores
    GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_0 | GPIO_PIN_1, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);

    while(1)
    {
        state1();
        delay();
        state2();
        delay();
        state3();
        delay();
        state4();
        delay();
       // for(ui32Loop = 0; ui32Loop < 200000; ui32Loop++)
        //{
        //}
    }
}
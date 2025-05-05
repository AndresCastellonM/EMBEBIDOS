//LABO4 TIMERS EJERCICIO2Y3
//*****************************************************************************
// LIBRERIAS
//<stdint.h> y <stdbool.h>: Para tipos de datos como uint32_t y bool.
//"inc/hw_ints.h", "inc/hw_memmap.h", "inc/hw_types.h": Para definiciones de hardware.
//"driverlib/*.h": Para funciones de control de periféricos como GPIO, UART y temporizadores.
//*****************************************************************************

#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_ints.h"
#include "inc/hw_memmap.h"
#include "inc/hw_types.h"
#include "driverlib/debug.h"
#include "driverlib/fpu.h"
#include "driverlib/gpio.h"
#include "driverlib/interrupt.h"
#include "driverlib/pin_map.h"
#include "driverlib/rom.h"
#include "driverlib/rom_map.h"
#include "driverlib/sysctl.h"
#include "driverlib/timer.h"
//#include "driverlib/uart.h"
//#include "utils/uartstdio.h"

//****************************************************************************
// VARIABLES GLOBALES
//****************************************************************************
// ALMACENA LA VELOCIDAD DEL RELOJ DEL SISTEMA (FRECUENCIA DEL MICROCONTROLADOR)
uint32_t g_ui32SysClock; 
// SE UTILIZA COMO UN INDICADOR PARA EL MANEJO DE INTERRUPCIONES (EN ESTE CASO, PARA LTERNAR EL ESATDO DE UN LED)
uint32_t g_ui32Flags;


// Contador que indica cuantos LEDs estan encendidos.
uint32_t g_ui32LedIndex = 0;


// Estado del temporizador (0 = 0.5 segundos, 1 = 1 segundo)
uint32_t g_ui32TimerState = 0;

// Variable para almacenar el estado anterior del boton
bool g_bLastButtonState = false;


//*****************************************************************************
//ESTA ES UNA RUTINA VACIA QUE SE LLAMA SI OSURRE UN ERROR EN LA LIBRERIA DEL MICROCONTROLADOR SOLO ESTA PRESENTE EN EL MODO DEPURACION
//*****************************************************************************
#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
}
#endif

//*****************************************************************************
//HANDLER DE INTERRUPCION DEL TIMER 0 / Manejador de interrupcion
//*****************************************************************************
void Timer0IntHandler(void) {
    // Limpia la interrupción del temporizador 0.
    MAP_TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    // Si g_ui32LedIndex llega a 4, apaga todos los LEDs y reinicia el ciclo.
    if (g_ui32LedIndex >= 4)
    {
        // Apaga todos los LEDs.
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1, 0);
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0, 0);

        // Reinicia el índice.
        g_ui32LedIndex = 0;
    }
    else
    {
        // Acumula los LEDs encendidos:
        // Encendemos el LED correspondiente sin apagar los anteriores.
        if (g_ui32LedIndex == 0)
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);  // Enciende LED 1 (PN1)
        else if (g_ui32LedIndex == 1)
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);  // Enciende LED 2 (PN0)
        else if (g_ui32LedIndex == 2)
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);  // Enciende LED 3 (PF4)
        else if (g_ui32LedIndex == 3)
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);  // Enciende LED 4 (PF0)

        // Incrementa el índice del LED.
        g_ui32LedIndex++;
    }
}

//*****************************************************************************
//EL CODIGO EN LA FUNCION MAIN CONFIGURA Y HABILITA EL TEMPORIZADOR Y EL LED
//*****************************************************************************
int main(void) {
    // Configura el sistema para que corra a 120 MHz usando el PLL.
    g_ui32SysClock = MAP_SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                             SYSCTL_OSC_MAIN |
                                             SYSCTL_USE_PLL |
                                             SYSCTL_CFG_VCO_240), 120000000);

    // Habilita los puertos GPIO que se usan para los LEDs y el boton.
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);  // Habilita el puerto GPIO para el boton (PJ0).

    // Habilita los pines GPIO para los LEDs (PN0, PN1 y PF4, PF0).
    MAP_GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1);
    MAP_GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_4 | GPIO_PIN_0);

    // Configura el pin PJ0 como entrada para el boton.
    MAP_GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_0);
    MAP_GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_0, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);  // Configura resistencia pull-up.

    // Habilita el perifÃ©rico utilizado por el temporizador.
    MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);

    // Habilita las interrupciones del procesador.
    MAP_IntMasterEnable();

    // Configura el temporizador 0 en modo periÃ³dico.
    MAP_TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);
    MAP_TimerLoadSet(TIMER0_BASE, TIMER_A, g_ui32SysClock*0.5);  // Temporizador a 0.5 segundos inicialmente.

    // Configura la interrupcion para el timeout del temporizador 0.
    MAP_IntEnable(INT_TIMER0A);
    MAP_TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    // Habilita el temporizador.
    MAP_TimerEnable(TIMER0_BASE, TIMER_A);

    // Bucle infinito mientras el temporizador corre.
    while(1)
    {
        // Lee el estado actual del boton.
        bool bButtonState = MAP_GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0;

        // Si el boton esta presionado y no estaba presionado en la iteracion anterior.
        if (bButtonState && !g_bLastButtonState)
        {
            // Alterna entre los dos tiempos del temporizador.
            g_ui32TimerState = !g_ui32TimerState;

            // Cambia el periodo del temporizador segÃºn el estado.
            if (g_ui32TimerState == 0)
            {
                // Ajusta el temporizador a 0.5 segundos.
                MAP_TimerLoadSet(TIMER0_BASE, TIMER_A, g_ui32SysClock*0.5);
            }
            else
            {
                // Ajusta el temporizador a 1 segundo.
                MAP_TimerLoadSet(TIMER0_BASE, TIMER_A, g_ui32SysClock*1);
            }
        }

        // Guarda el estado del boton para la proxima iteracion.
        g_bLastButtonState = bButtonState;
    }
}

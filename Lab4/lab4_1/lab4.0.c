//LABO4 TIMERS
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
    // BORRA (LIMPIA) LA INTERRUPCION DEL TEMPORIZADOR PARA EVITAR QUE SE REPITA SIN CONTROL
    MAP_TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    // ALTERNA EL PRIMER BIT DE g_ui32Flags. ESTO CAMBIA ENTRE 1 Y0 CADA VEZ QUE SE EJECUTA LA INTERRUPCION
    HWREGBITW(&g_ui32Flags, 0) ^= 1;

    // UTILIZA EL VALOR DEL FLAG PARA ENCENDER O APAGAR EL LED EN EL PIN GPIO
    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, HWREGBITW(&g_ui32Flags, 0) ? GPIO_PIN_1 : 0);
}

//*****************************************************************************
//EL CODIGO EN LA FUNCION MAIN CONFIGURA Y HABILITA EL TEMPORIZADOR Y EL LED
//*****************************************************************************
int main(void) {
    // AQUI SE CONFIGURA EL RELOJ DEL SISTEMA PARA QUE FUNCIONE A 120MHZ USANDO EL PLL (PHASE LOCKED LOOP)
    g_ui32SysClock = MAP_SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
        SYSCTL_OSC_MAIN |
        SYSCTL_USE_PLL |
        SYSCTL_CFG_VCO_240), 120000000);

// HABILITA EL PUERTO GPIO QUE SE UTILIZA PARA EL LED INTEGRADO EN LA PLACA
//Puerto N
MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);

// HABILITA EL PIN GPIO PARA EL LED (PN1).
MAP_GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_1);

///////Configuración del temporizador (Timer0) PERIODICO :////////////////////////
// HABILITA EL PERIFERICO UTILIZADO EN ESTE EJEMPLO (TEMPORIZADOR TIMER0)
MAP_SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);

// ACTIVA LAS INTERRUPCIONES DEL PROCESADOR
MAP_IntMasterEnable();

// AQUI SE CONFIGURA EL TEMPORZADOR PARA QUE SEA PERIODICO (ES DECIR, QUE GENERE UNA INTERRUPCION AINTERVALO REGULARES) Y SE AJUSTA A LA DURACION DEL TEMPORIZADOR PARA QUE ACTIVE CADA MEDIO SEGUNDO (ASUMIENDO QUE g_ui32SysClock ES 120 MHZ
MAP_TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);


////////CALCULO DEL TIEMPO DE PERIODO SEGUN SEA NECESARIO PARA 1 SEGUNDO, 2 SEGUNDOS, 5 SEGUNDOS :////////////////////////
//g_ui32SysClock es la frecuencia del reloj del sistema (120,000,000 Hz).
//Ciclos=Frecuencia del reloj×Tiempo deseado => Ciclos=Frecuencia del reloj/(1/Tiempo deseado)

MAP_TimerLoadSet(TIMER0_BASE, TIMER_A, g_ui32SysClock / 1); // AJUSTA EL PERIODO SEGUN SEA NECESARIO PARA 1 SEGUNDO
//MAP_TimerLoadSet(TIMER0_BASE, TIMER_A, g_ui32SysClock / 0.5);//AJUSTA EL PERIODO SEGUN SEA NECESARIO PARA 2 SEGUNDO
//MAP_TimerLoadSet(TIMER0_BASE, TIMER_A, g_ui32SysClock / 0.2);  //AJUSTA EL PERIODO SEGUN SEA NECESARIO PARA 5 SEGUNDO

///////////// HABILITACION DE INTERRUPCIONES //////////////////////////
// SE HABILITA LA INTERRUPCION DEL TEMPORIZADOR Y EL PROPIO TEMPORIZADOR PARA QUE COMIENCE A CONTAR
//Interrupccion del temporizador Timer0A
MAP_IntEnable(INT_TIMER0A);
MAP_TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);
// ACTIVA EL TEMPORIZADOR
MAP_TimerEnable(TIMER0_BASE, TIMER_A);

// BUCLE ETERNO MIENTRAS SE EJECUTA EL TEMPORIZADOR
while(1)
{
}
}

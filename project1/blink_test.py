from gpiozero import LED
from signal import pause

led = LED(22)

led.on()

pause()

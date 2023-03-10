"""
File:   Project1_LEDs.py
Author: Austin Sands
Date:   02/10/2023
Description: This python script was written and tested on a Raspberry Pi 3B. 
This program requires two LEDs, one connected to GPIO17 (physical pin 11) and GPIO5 (physical pin 29),
as well as, two buttons, one connected to GPIO27 (physical pin 13) and GPIO6 (physical pin 31).
"""

from gpiozero import LED
from gpiozero import PWMLED
from gpiozero import Button
import time

"""
Declare variables and functions for blinking LED
"""
button_blink = Button(27)
led_blink = LED(17)

clock_start = time.time()
blink_start = clock_start
time_delta = 0

clock_paused = False
cycle_time_passed = 0

blink_frequency = 1

def change_speed():
    global blink_frequency

    blink_frequency -= 0.21
    if blink_frequency <= 0:
        blink_frequency = 1

    print("Blink Frequency: " + str(blink_frequency) + "\n")

def stop_start():
    global clock_paused, cycle_time_passed, clock_start, time_delta

    #if clock is not paused when called, save the time in the cycle that has already passed
    #I use this variable to resume the light cycle at the exact time it was paused
    if not clock_paused:
        cycle_time_passed = time_delta
        print("Clock paused! Time in cycle paused: " + str(cycle_time_passed) + "\n")
    #if the clock was paused when called, subtract cycle time passed from current time
    #this will allow clock to resume at same point in the cycle when paused
    elif clock_paused:
        clock_start = time.time() - cycle_time_passed
        print("Clock resumed!\n")

    #toggle clock_paused variable
    clock_paused = not clock_paused
"""
End variables and functions for blinking LED
"""
"""
Declare variables and functions for PWM LED
"""
led_pwm = PWMLED(5)
button_pwm = Button(6)

dc_coefficient = 4

def change_duty_cycle():
    global dc_coefficient
    dc_coefficient -= 1
    if dc_coefficient < 0:
        dc_coefficient = 4

    print("Current brightness setting: " + str(dc_coefficient * 0.25) + "\n")
"""
End variables and functions for PWM LED
"""
            
while True:
    time_delta = time.time() - clock_start
    blink_delta = time.time() - blink_start

    if blink_delta >= blink_frequency:
        led_blink.toggle()
        blink_start = time.time()

    button_blink.when_pressed = stop_start
    button_pwm.when_pressed = change_duty_cycle

    led_pwm.value = dc_coefficient * 0.25
    
    if clock_paused:
        continue

    if time_delta < 5:
        continue

    change_speed()
    clock_start = time.time()

#!/usr/bin/env python3          
#https://roboticsbackend.com/raspberry-pi-gpio-interrupts-tutorial/#:~:text=Use%20the%20%EE%80%80wait_for_edge()wait_for_edge()function%EE%80%81                     
import signal                   
import sys
import RPi.GPIO as GPIO

BUTTON_GPIO = 16
LED_GPIO = 20

last_LED_state = 0

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_pressed_callback(channel):
    global last_LED_state
    GPIO.output(LED_GPIO, not last_LED_state)
    last_LED_state = not last_LED_state

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED_GPIO, GPIO.OUT)

    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, 
            callback=button_pressed_callback, bouncetime=200)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
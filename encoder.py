from gpiozero import Button
import time

# Rotary encoder pins
pin_a = Button(2, pull_up=True)
pin_b = Button(3, pull_up=True)

# Event handlers
def pin_a_rising():
    if pin_b.is_pressed:
        print("-1")  # Clockwise turn

def pin_b_rising():
    if pin_a.is_pressed:
        print("1")   # Anti-clockwise turn

# Register event handlers
pin_a.when_pressed = pin_a_rising
pin_b.when_pressed = pin_b_rising

print("Turn the knob, press Enter to quit.")
input()

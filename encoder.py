from gpiozero import Button
import time

# Connect your encoder pins to GPIO 20 and 21
pin_a = Button(20, pull_up=True)
pin_b = Button(21, pull_up=True)

# Initialize variables
previous_state = None
rpm = 0
count = 0
start_time = time.time()

def update_rpm():
    global rpm, count, start_time
    elapsed_time = time.time() - start_time
    rpm = (count / elapsed_time) * 60
    start_time = time.time()
    count = 0

def pin_a_rising():
    global count
    if pin_b.is_pressed:
        count += 1

def pin_b_rising():
    global count
    if pin_a.is_pressed:
        count += 1

# Register event handlers
pin_a.when_pressed = pin_a_rising
pin_b.when_pressed = pin_b_rising

while True:
    update_rpm()
    print(f"RPM: {rpm:.2f}")
    time.sleep(1)

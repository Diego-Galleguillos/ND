from gpiozero import Button, RotaryEncoder
import time
from adafruit_motorkit import MotorKit
from func import steps_for_angle
kit = MotorKit()
# Connect your encoder pins to GPIO 20 and 21
pin_b = Button(20, pull_up=True)
pin_a = Button(21, pull_up=True)

pin_2b = Button(19, pull_up=True)
pin_2a = Button(16, pull_up=True)

# Initialize variables
previous_state = None
rpm = 0
count = 0
start_time = time.time()

def move_angle(steps_per_turn, angle, kit, motor_number):
    global count, count2
    steps = steps_for_angle(steps_per_turn, angle)
    count = 0
    count2 = 0
    if motor_number == 1:
        while count < steps:
            print(count)
            kit.motor1.throttle = (steps_per_turn - count)/(steps_per_turn*2)
        kit.motor1.throttle = 0
    else:
        while count2 < steps:
            print(count)
            kit.motor2.throttle = (steps_per_turn - count2)/(steps_per_turn*2)
        kit.motor2.throttle = 0

def update_rpm():
    global rpm, count, start_time
    elapsed_time = time.time() - start_time
    rpm = (count / elapsed_time) * 60 / (100.37 * 6)
    start_time = time.time()


def pin_a_rising():
    global count, previous_state
    current_state = (pin_a.is_pressed, pin_b.is_pressed)
    count += 1

def pin_b_rising():
    global count, previous_state
    current_state = (pin_a.is_pressed, pin_b.is_pressed)
    count += 1
# Register event handlers
pin_a.when_pressed = pin_a_rising
pin_b.when_pressed = pin_b_rising



# Initialize variables
previous_state2 = None
rpm2 = 0
count2 = 0
start_time2 = time.time()

def update_rpm2():
    global rpm2, count2, start_time2
    elapsed_time = time.time() - start_time2
    rpm2 = (count2 / elapsed_time) * 60 / (100.37 * 6)
    start_time2 = time.time()


def pin_a_rising2():
    global count2, previous_state2
    current_state = (pin_2a.is_pressed, pin_2b.is_pressed)
    count2 += 1

def pin_b_rising2():
    global count2, previous_state2
    current_state = (pin_2a.is_pressed, pin_2b.is_pressed)
    count2 += 1
# Register event handlers
pin_2a.when_pressed = pin_a_rising2
pin_2b.when_pressed = pin_b_rising2


kit.motor1.throttle = 0.2
kit.motor2.throttle = 0.2
c = 0

while count < 600:
    update_rpm()
    update_rpm2()
    print(f"RPM: {rpm:.2f}, Count: {count} ")
    print(f"RPM2: {rpm2:.2f}, Count2: {count2} ")
    time.sleep(0.001)
    c = c + 1

kit.motor1.throttle = 0.0


kit.motor2.throttle = 0.0

time.sleep(1)
move_angle(600, 90, kit, 1)

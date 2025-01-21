from gpiozero import Button
import time
from adafruit_motorkit import MotorKit

def steps_for_angle(steps_per_turn, angle):
    steps = (angle/360) * steps_per_turn
    return steps

kit = MotorKit()

# Connect your encoder pins to GPIO 20 and 21
pin_b = Button(20, pull_up=True)
pin_a = Button(21, pull_up=True)

pin_2b = Button(19, pull_up=True)
pin_2a = Button(16, pull_up=True)

# Initialize variables
encoder_position_1 = 0
encoder_position_2 = 0
last_state_a_1 = pin_a.is_pressed
last_state_b_1 = pin_b.is_pressed
last_state_a_2 = pin_2a.is_pressed
last_state_b_2 = pin_2b.is_pressed

def move_angle(steps_per_turn, angle, kit, motor_number):
    global encoder_position_1, encoder_position_2
    steps = steps_for_angle(steps_per_turn, angle)
    encoder_position_1 = 0
    encoder_position_2 = 0
    if motor_number == 1:
        while encoder_position_1 < steps:
            print(encoder_position_1)
            kit.motor1.throttle = (steps_per_turn - encoder_position_1) / (steps_per_turn * 2)
        kit.motor1.throttle = 0
    else:
        while encoder_position_2 < steps:
            print(encoder_position_2)
            kit.motor2.throttle = (steps_per_turn - encoder_position_2) / (steps_per_turn * 2)
        kit.motor2.throttle = 0

def update_encoder_position_1():
    global encoder_position_1, last_state_a_1, last_state_b_1

    # Read current state of pin A and B
    current_state_a = pin_a.is_pressed
    current_state_b = pin_b.is_pressed
    
    # Check if there is any state change in encoder A
    if current_state_a != last_state_a_1:
        # Determine the direction by looking at the state of pin B
        if current_state_a != current_state_b:
            encoder_position_1 += 1  # Clockwise
        else:
            encoder_position_1 -= 1  # Counterclockwise

    # Update the last known state
    last_state_a_1 = current_state_a
    last_state_b_1 = current_state_b

def update_encoder_position_2():
    global encoder_position_2, last_state_a_2, last_state_b_2

    # Read current state of pin A and B
    current_state_a = pin_2a.is_pressed
    current_state_b = pin_2b.is_pressed
    
    # Check if there is any state change in encoder A
    if current_state_a != last_state_a_2:
        # Determine the direction by looking at the state of pin B
        if current_state_a != current_state_b:
            encoder_position_2 += 1  # Clockwise
        else:
            encoder_position_2 -= 1  # Counterclockwise

    # Update the last known state
    last_state_a_2 = current_state_a
    last_state_b_2 = current_state_b

# Main loop
kit.motor1.throttle = 0.2
kit.motor2.throttle = 0.2
c = 0

while encoder_position_1 < 600:
    update_encoder_position_1()
    update_encoder_position_2()
    print(f"Encoder Position 1: {encoder_position_1}")
    print(f"Encoder Position 2: {encoder_position_2}")
    time.sleep(0.01)
    c += 1

kit.motor1.throttle = 0.0
kit.motor2.throttle = 0.0

time.sleep(1)
move_angle(600, 90, kit, 1)

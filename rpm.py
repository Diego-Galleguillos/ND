import time

# Variables to store pulse count and time
pulse_count = 0
start_time = time.time()

# Event handlers
def pin_a_rising():
    global pulse_count
    if pin_b.is_pressed:
        pulse_count += 1

def pin_b_rising():
    global pulse_count
    if pin_a.is_pressed:
        pulse_count += 1

# Register event handlers
pin_a.when_pressed = pin_a_rising
pin_b.when_pressed = pin_b_rising

# Calculate RPM
def calculate_rpm():
    elapsed_time = time.time() - start_time
    rpm = (pulse_count / elapsed_time) * 60
    return rpm

# Main loop
while True:
    print(f"RPM: {calculate_rpm()}")  # Print RPM
    time.sleep(1)

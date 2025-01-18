import time
from gpiozero import RotaryEncoder
from adafruit_motorkit import MotorKit

kit = MotorKit()
encoder = RotaryEncoder(21, 20)

c = 0
kit.motor1.throttle = 0.2


while c < 5:
    print(encoder.steps)
    c += 1
    time.sleep(1)

kit.motor1.throttle = 0

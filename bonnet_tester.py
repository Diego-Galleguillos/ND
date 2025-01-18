# sudo pip3 install adafruit-circuitpython-motorkit
import time
from adafruit_motorkit import MotorKit
kit = MotorKit()

# Start the motor on motor1
kit.motor1.throttle = 0.2  # Full speed forward

time.sleep(2)

kit.motor1.throttle = 0.0

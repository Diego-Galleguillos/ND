# sudo pip3 install adafruit-circuitpython-motorkit

from adafruit_motorkit import MotorKit
kit = MotorKit()

# Start the motor on motor1
kit.motor1.throttle = 1.0  # Full speed forward

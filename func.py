from adafruit_motorkit import MotorKit
import time


def steps_for_angle(steps_per_turn, angle):
    steps = (angle/360) * steps_per_turn
    return steps

def move_angle(steps_per_turn, angle, kit, motor_number):
    global count, count2
    steps = steps_for_angle(steps_per_turn, angle)
    count = 0
    count2 = 0
    if motor_number == 1:
        while count < steps:
            print(count)
            kit.motor1.throttle = (steps_per_turn - count)/steps_per_turn
        kit.motor1.throttle = 0
    else:
        while count2 < steps:
            kit.motor2.throttle = (steps_per_turn - count2)/steps_per_turn
        kit.motor2.throttle = 0

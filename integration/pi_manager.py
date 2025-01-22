import threading
from gpiozero import Button, RotaryEncoder
import time
from adafruit_motorkit import MotorKit
import socket



def steps_for_angle(steps_per_turn, angle):
    steps = (angle/360) * steps_per_turn
    return steps

class Pi_manager:
    def __init__(self, id):
        self.id = id
        self.kit = MotorKit()
        self.enc1 = RotaryEncoder(0, 1, max_steps=1200)
        self.enc2 = RotaryEncoder(16, 19, max_steps=1200)
        self.previous_state = None
        self.count = 0
        self.start_time = time.time()
        self.previous_state2 = None
        self.count2 = 0
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('192.168.0.101', 9999))
        self.message = "Initial message from server."
        self.steps_per_turn = 300

    def move_angle(self, steps_per_turn, angle, motor_number, direction = 1):
        steps = steps_for_angle(steps_per_turn, angle)
        self.count = 0
        self.count2 = 0
        if motor_number == 1:
            while self.count < steps:
                print(self.count, self.count2, "in loop")
                self.kit.motor1.throttle = direction * (steps_per_turn - self.count)/(steps_per_turn*2)
                if   (steps_per_turn - self.count)/(steps_per_turn*2) < 0.15:
                    self.kit.motor1.throttle = 0.15 * direction
                time.sleep(0.001)
            self.kit.motor1.throttle = 0
        else:
            while self.count2 < steps:
                print(self.count2)
                self.kit.motor2.throttle = (steps_per_turn - self.count2)/(steps_per_turn*2) * direction
                time.sleep(0.001)
            self.kit.motor2.throttle = 0

    def receive_message(self):
        while "exit" not in self.message:
            data = self.client_socket.recv(1024).decode()
            self.message = data
            print(self.message)

            if "exit" in self.message:
                self.stop()
                break
            try:
                if int(self.message[0]) == self.id or int(self.message[0]) == 0:
                    print("taking step")
                    self.take_steps(self.steps_per_turn, int(self.message[2]), 1)
            except:
                print("message too short")


    def take_steps(self, steps_per_turn, number_of_steps, motor_number):
        self.move_angle(steps_per_turn, number_of_steps*360, motor_number)

    def enc1_rotated(self):
        self.count = self.enc1.steps
        
    def enc2_rotated(self):
        self.count2 = self.enc2.steps


    def start(self):
        self.enc1.when_rotated = self.enc1_rotated
        self.enc2.when_rotated = self.enc2_rotated

        self.client_handler = threading.Thread(target=self.receive_message)
        self.client_handler.start()

    def stop(self):
        self.client_socket.close()
        self.client_handler.join()


if __name__ == "__main__":
    id = int(input("Enter the id of the pi: "))
    pi = Pi_manager(id)
    pi.start()

    while True:
        try:
            pass
        except KeyboardInterrupt:
            pi.stop()
            break


import paho.mqtt.client as mqtt
import time
import signal                   
import sys
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit
import random

class Robot:
    def __init__(self):
        self.kit = MotorKit()
        self.encoder = 16
        #self.LED_GPIO = 20
        self.last_LED_state = 0
        self.broker = "YOUR_PC_IP"
        self.client_id = f'pi-{random.randint(0, 1000)}'
        self.client = mqtt.Client(client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker)
        self.client.subscribe("com/topic")
        self.client.loop_start()
        self.last_instruction = "stop"

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

    def on_message(self, client, userdata, message):
        print(f"Received message: {message.payload.decode()} on topic {message.topic}")
        self.last_instruction = message.payload.decode()
    
    def signal_handler(self, sig, frame):
        self.client.loop_stop()
        self.client.disconnect()
        GPIO.cleanup()
        sys.exit(0)
    
    def run(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.encoder, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #GPIO.setup(self.LED_GPIO, GPIO.OUT)
        GPIO.add_event_detect(self.encoder, GPIO.FALLING, callback=self.encoder_callback, bouncetime=200)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.pause()
    
    def encoder_callback(self, channel):
        pass

    def move(self, direction):
        if direction == "forward":
            self.kit.motor1.throttle = 1.0
            self.kit.motor2.throttle = 1.0
        elif direction == "backward":
            self.kit.motor1.throttle = -1.0
            self.kit.motor2.throttle = -1.0
        elif direction == "left":
            self.kit.motor1.throttle = 1.0
            self.kit.motor2.throttle = -1.0
        elif direction == "right":
            self.kit.motor1.throttle = -1.0
            self.kit.motor2.throttle = 1.0
        elif direction == "stop":
            self.kit.motor1.throttle = 0
            self.kit.motor2.throttle = 0
    
    def run_robot(self):
        while self.last_instruction != "shutdown":
            self.move(self.last_instruction)
            time.sleep(0.1)
        self.shutdown()
    
    def shutdown(self):
        self.kit.motor1.throttle = 0
        self.kit.motor2.throttle = 0
        self.client.loop_stop()
        self.client.disconnect()
        GPIO.cleanup()
        sys.exit(0)

if __name__ == '__main__':
    robot = Robot()
    robot.run()
    robot.run_robot()
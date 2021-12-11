import RPi.GPIO as GPIO
import time

motorPin = 5
motor1 = 6
motor2 = 13
GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)
GPIO.setup(motorPin,GPIO.OUT)
GPIO.setup(motor1,GPIO.OUT)
GPIO.setup(motor2,GPIO.OUT)

GPIO.output(motor1, 0)
GPIO.output(motor2, 0)
GPIO.output(motorPin, 0)
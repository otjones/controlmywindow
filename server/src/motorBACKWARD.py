import RPi.GPIO as GPIO
import time

motorPin = 5
motor1 = 6
motor2 = 13
endPin = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(endPin,GPIO.IN, pull_up_down=GPIO.PUD_UP)

if GPIO.input(endPin):

    GPIO.setwarnings(False)
    GPIO.setup(motorPin,GPIO.OUT)
    GPIO.setup(motor1,GPIO.OUT)
    GPIO.setup(motor2,GPIO.OUT)

    GPIO.output(motor1, 0)
    GPIO.output(motor2, 1)
    GPIO.output(motorPin, 1)

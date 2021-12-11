import RPi.GPIO as GPIO
import time

motorPin = 5
motor1 = 6
motor2 = 13
endPin1 = 4
endPin2 = 16
GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)
GPIO.setup(motorPin,GPIO.OUT)
GPIO.setup(motor1,GPIO.OUT)
GPIO.setup(motor2,GPIO.OUT)
GPIO.setup(endPin1,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(endPin2,GPIO.IN, pull_up_down=GPIO.PUD_UP)

end = False

def motorStop(end):
    GPIO.output(motor1, 0)
    GPIO.output(motor2, 0)
    GPIO.output(motorPin, 0)
    end = True
    return end

while True:
    if not GPIO.input(endPin1) or not GPIO.input(endPin2):
        if end:
            pass
        else:
            end = motorStop(end)
    else:
        end = False
        pass
    time.sleep(0.01)

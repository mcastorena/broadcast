import RPi.GPIO as GPIO
import time
import threading
import config
import array
from struct import pack
import serial


portLocation = '/dev/ttyACM0'
ser = serial.Serial(port=portLocation, baudrate=115200)



class ultraSensor(threading.Thread):
    def __init__(self, s, c):
        threading.Thread.__init__(self)
        GPIO.setmode(GPIO.BCM)
        self.TRIG = 14
        self.ECHO = 24
        self.serialSem = s
        self.condition = c

    def payload(self, code, distance, offset, sensor1, sensor2, sensor3):
        ch = 0
        length = 12
        pay = pack('hHHHHH', code, distance, offset, sensor1, sensor2, sensor3)
        a = array.array('b', pay)
        a = a.tobytes()

        for i in range(0, 12):
            ch = (ch + a[i]) % 256

        pay = pack('BBB', 67, 79, 12) + pay + pack('B', ch)
        return pay

    def run(self):
        print("Thread started: getting sensor distance")
        GPIO.setmode(GPIO.BCM)

        while True:
            time.sleep(0.5)

            GPIO.setup(self.TRIG, GPIO.OUT)
            GPIO.output(self.TRIG, 0)

            GPIO.setup(self.ECHO, GPIO.IN)

            time.sleep(0.1)

            GPIO.output(self.TRIG, 1)
            time.sleep(0.00001)
            GPIO.output(self.TRIG, 0)

            while GPIO.input(self.ECHO) == 0:
                pass
            pulse_start = time.time()

            while GPIO.input(self.ECHO) == 1:
                pass
            pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)
            print "Distance:", distance, "cm"



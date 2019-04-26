import serial
from struct import *
import array
from sys import stdout
from threading import Timer, Thread, Semaphore
from time import sleep

sem = Semaphore()

code = 1
distance = 100
offset = 20
sensor1 = 0
sensor2 = 0
sensor3 = 0
globalpay = None


# C  = 67
# O  = 81
# size = 12
# Data
#    uint16_t code;
#    int16_t distance, offset;
#    int16_t sensor1_dist;
#    int16_t sensor2_dist;
#    int16_t sensor3_dist;
# checksum


def payload(code, distance, offset, sensor1, sensor2, sensor3):
    ch = 0
    length = 12
    pay = pack('Hhhhhh', code, distance, offset, sensor1, sensor2,
               sensor3)  # pack as (unsigned short, short, short, short, short, short)
    a = array.array('b', pay)
    a = a.tobytes()

    for i in range(0, length):  # compute check sum
        ch = (ch + a[i]) % 256

    pay = pack('BBB', 67, 79, 12) + pay + pack('B', ch)
    return pay


ser = serial.Serial(port='COM3', baudrate=115200)  # open serial port for send
ser.isOpen()  # check if serial port is open


def readSerial():
    while 1:
        sleep(0.5)
        sem.acquire()
        pay = ser.read_all()
        sem.release()
        if(pay != b''):
            print("running: ", pay)

# Prompts user for input and send
def Sensors():
    code = input("Code: ")
    distance = input("Distance: ")
    offset = input("Offset: ")
    print("Inputs:\t",code, distance, offset)
    # sensor1 = input("Sensor1: ")
    # sensor2 = input("Sensor2: ")
    # sensor3 = input("Sensor3: ")
    pay = payload(int(code), int(distance), int(offset), sensor1, sensor2, sensor3)  # get payload
    print("payload: ", pay)  # print payload
    sem.acquire()  # get semaphore lock
    ser.write(pay)  # write payload to serial port
    sem.release()  # release semaphore lock
    t = Timer(0.5, Sensors)  # run sensors every 0.5 seconds
    t.start()


thread = Thread(target=readSerial)
thread.start()
Sensors()
thread.join()







import threading
from time import sleep
import serial

#from aruco_calculations import ArucoCalculator
from codeListener import codeListener
from ultraSensor import ultraSensor
# Global variables
condition = threading.Condition()
printSem = threading.Semaphore()
serialSem = threading.Semaphore()

# size in meters of aruco marker
ARUCO_SQUARE_WIDTH = 0.141  # formerly 0.152
CALIB_FILENAME = 'camera_calib.json'
portLocation = '/dev/ttyACM0'

ser = serial.Serial(port=portLocation, baudrate=115200)


def readSerial():
    while 1:
        sleep(1)
        serialSem.acquire()
        pay = ser.read_all()
        serialSem.release()
        if(pay != b''):                                                 # If not empty print
            printSem.acquire()
            print("running: ", pay)
            printSem.release()


if __name__ == "__main__":
    seconds_per_capture = 2                                             # Seconds per capture for Pi Camera

    #cameraThread = ArucoCalculator(seconds_per_capture, condition)                 # Create process threads
    teensyInterface = codeListener(serialSem, printSem, condition)
    distanceSensor = ultraSensor(serialSem, condition)

    #cameraThread.start()                                                # Start threads
    teensyInterface.start()
    distanceSensor.start()

    readThread = threading.Thread(target=readSerial())                  # Create thread to read serial

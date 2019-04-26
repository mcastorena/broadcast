import socket
import threading
import serial
import array
from struct import pack
from time import sleep

portLocation = 'COM11'

distance = 10
offset = 10
sensor1 = 0
sensor2 = 0
sensor3 = 0

sem = threading.Semaphore()
printSem = threading.Semaphore()
ser = serial.Serial(port=portLocation, baudrate=115200)


class codeListener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.code = None

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
        print("\nCode listener running\n")
        self.recvBroadcastCode()
        self.readSerial()


    def recvBroadcastCode(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)             # UDP socket
        sock.bind(('', 2000))                                               # Bind to localhost on port 2000

        data, senderAddr = sock.recvfrom(1500, 0)                           # Receive broadcast, buffer size 1500
        self.code = int( data.decode('UTF-8') )                                   # Save code
        print("\nBroadcast code received: ", self.code)
        self.writeCode()

    def writeCode(self):
        codePay = self.payload(self.code,0,0,0,0,0)                                      # Pack code as unsigned short
        sem.acquire()                                                       # Acquire semaphore lock
        ser.write(codePay)                                                  # Write code to serial
        sem.release()                                                       # Release semaphore lock
        print("\nBroadcast code written to serial")

    def readSerial(self):
        msgRecv = b''                                                      # Initialize msgRecv as b'0'
        while(b'Sensor Reading' or b'In BROADCAST' not in msgRecv):                                             # Read serial until a message is received
            sem.acquire()
            msgRecv = ser.read_all()                                        # Read from serial and store it in msgRecv
            sem.release()
        print("\nReceived: ", msgRecv)
        self.writeDistanceOffset()                                      # Call writeDistanceOffset


    def writeDistanceOffset(self):
        printSem.acquire()
        distance = input("Distance: ")
        offset = input("Offset: ")
        # sensor1 = input("Sensor1: ")
        # sensor2 = input("Sensor2: ")
        # sensor3 = input("Sensor3: ")
        print("Inputs:\t", distance, offset)
        printSem.release()
        pay = self.payload(self.code, int(distance), int(offset), sensor1, sensor2, sensor3)
        print("Writing payload to serial...")  # print payload
        sem.acquire()  # get semaphore lock
        ser.write(pay)  # write payload to serial port
        sem.release()  # release semaphore lock

def readSerial():
    while 1:
        sleep(1)
        sem.acquire()
        pay = ser.read_all()
        sem.release()
        if(pay != b''):
            printSem.acquire()
            print("running: ", pay)
            printSem.release()

myListener = codeListener()
myListener.start()
readThread = threading.Thread(target=readSerial())

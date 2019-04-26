import serial
from struct import unpack

portLocation = 'COM3'

ser = serial.Serial(port=portLocation, baudrate=115200)
msgRecv = b''
codeRecv = 0
while(codeRecv == 0):
    msgRecv = ser.read_all()
    print("Msg:\t", msgRecv)
    if(msgRecv != b''):
        codeRecv = unpack('h', msgRecv)
        print("Code received:\t", codeRecv)
print("Non-zero code received")
print(msgRecv)
ser.write(msgRecv)                                                           # Read code and send it back
print("Message sent")

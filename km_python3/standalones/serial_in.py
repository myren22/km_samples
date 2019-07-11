

####==================
"""This Code successfully reads the quick status of the ENG receiver from Kyle's Laptop"""
import time
import serial


a12 = [1,2,3,4,5,6,7,8,9]
a1= a12[len(a12)-1]
a2 = a12[:-1]
a3 = a12[-1:]

def serialBaseMethod(port='COM5'):
    ser = serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
    #continual feed
    while True:
        userIn= input('Send to Ser:\n')        
        if userIn =='exit':
            break
        ser.write(userIn.encode('ascii'))
        time.sleep(.01)
        serResponse = ser.read_all().decode('ascii')
        print("SerResponse:", serResponse)
        
        ser.write('?'.encode('ascii'))
        time.sleep(.02)
        serResponse = ser.read_all().decode('ascii')
        print('-')
        serResponse=serResponse[:150]
        print("RF Power dBm:", serResponse)
        
#         ser.write('h'.encode('ascii'))
#         time.sleep(.01)
#         serResponse = ser.read_all().decode('ascii')
#         print("High or Low?:", serResponse)
        
serialBaseMethod()

ser = serial.Serial('COM4', baudrate=9600)  # open serial port
print(ser.name)         # check which port was really used

a1 = chr(10)
b1 = chr(13)
a2 = 'NU010201d02b{}{}'.format(a1,b1).encode('ascii')
print('a2=',a2)

ser.write(a2)     # write a string

time.sleep(0.3)
a3 = ser.read_all()
print('recieve:',a3)

ser.close()  
####=================
def serialBaseMethod(port='COM5'):
    ser = serial.Serial(port)
    #continual feed
    while True:
        userIn= input('Send to Ser')
        if userIn =='exit':
            break
        ser.write(userIn)
        serResponse = ser.read_all()
        print("SerResponse:", serResponse)

serialReceived = a3
print('index[0]=',str(a3[0]))
print('index 24:26 - sigStr  ',a3[24:26])
print('index 49:51 - quality ',a3[48:50])
print('frequency[index 16:24]:',a3[16:24])
print('freq in dec', int(a3[16:24],16), 'KHz')
print('freq in MHz:', str(int(a3[16:24],16)/1000))

sigStrHex = serialReceived[24:26]
sigStrDec = int(sigStrHex, 16)
sigStrDec = sigStrDec -256
print('signal strength in dBm:',str(sigStrDec))

#get quickStatus signal Quality
aHex = serialReceived[48:50]
aDec = int(aHex, 16)
print('signal Quality Percent:',str(aDec))


#===============================================================================
# #  Open named port at "x, y, z,"
# with serial.Serial('COM4', 115200, timeout=5) as ser:  
#     x = ser.read()
#     print('x:',str(x))
#     s = ser.read(10)
#     print('s:',str(s))
#===============================================================================
    # ser.write(b'hello')
#     
#     x = ser.read()          # read one byte
#     print('X value: ',str(x))
#     s = ser.read(10)        # read up to ten bytes (timeout)
#     print('S value: ',str(s))
#     line = ser.readline()   # read a '\n' terminated line
#     print('Line value: ',str(line))
#     
#     ser.write(b'hello')
#     
#     x = ser.read()          # read one byte
#     print('X value: ',str(x))
#     s = ser.read(10)        # read up to ten bytes (timeout)
#     print('S value: ',str(s))
#     line = ser.readline()   # read a '\n' terminated line
#     print('Line value: ',str(line))
#     
#     ser.write(b'hello')
#     
#     x = ser.read()          # read one byte
#     print('X value: ',str(x))
#     s = ser.read(10)        # read up to ten bytes (timeout)
#     print('S value: ',str(s))
#     line = ser.readline()   # read a '\n' terminated line
#     print('Line value: ',str(line))
#     
#     ser.write(b'hello')
#     
#     x = ser.read()          # read one byte
#     print('X value: ',str(x))
#     s = ser.read(10)        # read up to ten bytes (timeout)
#     print('S value: ',str(s))
#     line = ser.readline()   # read a '\n' terminated line
#     print('Line value: ',str(line))
    
    
    
# serial.Serial() as ser:
    
# # #  Configuring ports later
# ser = serial.Serial()
# ser.baudrate = 115200
# ser.port = 'COM4'
# #  ser
# # has a value like: Serial<id=0xa81c10, open=False>(port='COM1', baudrate=19200, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0, rtscts=0)
# ser.open()
# 
# if(ser.is_open):
#     print('ser is open')
#     ser.write(b'hello')
#     
#     x = ser.read()          # read one byte
#     print('X value: ',str(x))
#     s = ser.read(10)        # read up to ten bytes (timeout)
#     print('S value: ',str(s))
#     line = ser.readline()   # read a '\n' terminated line
#     print('Line value: ',str(line))
# else:
#     print('ser is closed')
# 
# # returns True
# ser.close()
# ser.is_open

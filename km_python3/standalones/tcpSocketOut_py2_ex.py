'''
written for python 2.7 -> converted to 3.6

Created on Feb 12, 2018  - revised May 22

@author: Kyle

Objective:
-create a sending socket
-start independently the tcpSocketIn_py2_ex python program, 
    -this will listen on the same socket that is sending
    -it will print whenever a full message is made
    -then continue listening
-take user_input
-make a message out of input and send message
-loop back to taking user input
'''
import socket, time
import sys

# ETHERNET SOCKET
class mysocket:
    '''
    SOURCE: https://docs.python.org/2/howto/sockets.html
    -class mysocket taken from section called 'Using a Socket'
    
    ====     
    demonstration class only
      - coded for clarity, not efficiency
    '''       
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        while totalsent < len(msg):#MSGLEN
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        
        chunks = []
        bytes_recd = 0
#         while bytes_recd < len(msg):
#             chunk = self.sock.recv(min(len(msg) - bytes_recd, 2048))
#             if chunk == '':
#                 raise RuntimeError("socket connection broken")
#             chunks.append(chunk)
#             bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks)



def socket_out_sample1():    
    #===========================================================================
    # Echo Client socket code
    #===========================================================================
    latiDeg = 35.059567
    longDeg = -85.083972
    alt=392
    orientHYRP=[0,0,0,0]
    msgSend='{},{},{},{},{},{},{}'.format(latiDeg,longDeg,alt,orientHYRP[0],orientHYRP[1],orientHYRP[2],orientHYRP[3])
    #35.059567,-85.083972
    
    while True:    
        #user_input = str(raw_input('msg to send:\n>'))
        # print( 'Input:',user_input)
        # if 'exit-out' in user_input:
        #     #do stuff to close client as well as exit this loop
        #     break
        
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect the socket to the port where the server is listening
        ipAddr = '192.168.0.109' #localhost
        server_address = (ipAddr, 10000)

        print >>sys.stderr, 'connecting to %s port %s' % server_address
        sock.connect(server_address)
        #===#        
        try:            
            # Send data
            
            #set what string will be sent.            
            message = msgSend
#             print >>sys.stderr, 'sending "%s"' % message
            sock.sendall(message)
        
            # Look for the response
            amount_received = 0
            amount_expected = len(message)
            rebuilt_msg=''
            
            while amount_received < amount_expected:
                data = sock.recv(16)
                amount_received += len(data)
                rebuilt_msg = rebuilt_msg +data
                print >>sys.stderr, 'received "%s"' % data
            print( 'rebuilt msg:',rebuilt_msg)
            time.sleep(3)
        
        finally:
            print >>sys.stderr, 'closing socket'
            sock.close()
            
        if 'exit-in' in msgSend:    
            break
        
        # Update message contents for next loop
        latiDeg = latiDeg + 0.1
        msgSend='{},{},{},{},{},{},{}'.format(latiDeg,longDeg,alt,orientHYRP[0],orientHYRP[1],orientHYRP[2],orientHYRP[3])
    #===#
    
        
def socket_out_v2(user_input):
    ##==== Python 2.7
    '''
    Variables:
    -server_adress: str_name, int_port
    -message2send str
    
    *confirmation*
    -receive buff size
    -rebuilt_msg_str
    
     '''
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
    #===#        
    try:            
        #set what string will be sent.            
        message = user_input
        print >>sys.stderr, 'sending "%s"' % message
        sock.sendall(message)
    
        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        rebuilt_msg=''
        
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            rebuilt_msg = rebuilt_msg +data
            print >>sys.stderr, 'received "%s"' % data
        #print 'rebuilt msg:',rebuilt_msg
    
    finally:
        print >>sys.stderr, 'closing socket'
        sock.close()
    
        

if __name__ == '__main__':
    socket_out_sample1()
    pass


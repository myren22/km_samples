'''
written for python 3.6

Created on Feb 12, 2018 - revised May 22

@author: Kyle

obective:
-create listening socket
-periodically check for msg
-if complete messgage found, take it in and print
-if incomplete wait for full message to be written
-if no message keep waiting
-loop back to listening upon successful receive

Notes taken from: https://pymotw.com/3/socket/tcp.html under 'Echo Server

'''
import sys, os
import socket

print('start')


#  TCP ETHERNET SOCKET, taking in messages
def socket_in(ipAddr='localhost', portNum=10000):
    ''' 
    Create a TCP/IP socket - that keeps taking in messages.
    
    Variables:
    -ipAddr: a valid ip addr. Ex['localhost', '192.168.0.109']
    -portNum: a valid port number.   
    
    Object created:
    -socket.socket
    -connection
    -client_address
    -data    
    -message
    '''
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    # Bind the socket to the port
    server_address = (ipAddr,portNum)
    print('starting up on addr {} port {}'.format(*server_address))
    sock.bind(server_address)    
    # Listen for incoming connections
    sock.listen(1)    
    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
        complete_message=''        
        try:
            print('connection from', client_address)        
            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(32)
                print('received {!r}'.format(data))
                if data:
                    print('sending data back to the client')
#                     connection.sendall(data)
                    dataDecode = data.decode('utf-8')
                    complete_message+=dataDecode
                else:
                    print('no data from', client_address)
                    break
                
        finally:
            print('Complete Message:\n>', complete_message)
            connection.close()
        
        #if shutdown message recieved from client, exit. Let socket stay closed.
        if 'exit-in' in complete_message:    
            break
    print('Socket connection closed and no longer taking messages.')

if __name__ == '__main__':
    socket_in(ipAddr='localhost', portNum=6789)
    print('End of Program')
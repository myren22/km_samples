'''
written for python 2.7

Created on Feb 12, 2018 - revised May 22

@author: Kyle

obective:
-create LISTENING socket
-periodically check for msg
-if complete messgage found, take it in and print
-if incomplete wait for full message to be written
-if no message keep waiting
-loop back to listening upon successful receive

Notes taken from: https://pymotw.com/2/socket/tcp.html under 'Echo Server'
'''
import sys, os
import socket

print('start')


#  ETHERNET SOCKET
def socket_in_v1():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #------#
    
    # Bind the socket to the port
    server_address = ('localhost', 10000)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
        # >>sys.stderr  #this makes the following text/str red. 
        # sys.stderror seems like a conditional statement.
        #'starting up on {0} port {0}'.format(server_address) ==python3
    sock.bind(server_address)
    #------#
    
    # Listen for incoming connections
    sock.listen(1)
    
    while True:
        # Wait for a connection
        print >>sys.stderr, 'waiting for a connection'
        connection, client_address = sock.accept()
        complete_message=''
        #------#
        
        try:
            print >>sys.stderr, 'connection from', client_address
        
            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(32)
                print >>sys.stderr, 'received "%s"' % data
                if data:
                    print >>sys.stderr, 'sending data back to the client'
                    connection.sendall(data)
                    complete_message+=data
                else:
                    print >>sys.stderr, 'no more data from', client_address
                    break
                
        finally: #this will occur after try
            # Clean up the connection
            #print'Clean up connection -conn.close'
            connection.close()
        
        #if shutdown message recieved from client
        if 'exit-in' in complete_message:    
                break
            
def socket_in_v2():
    ''' 
    Variables:
    -server_adress: str_name, int_port      
    '''
    #socket/self?
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ipAddr = '192.168.0.109' #localhost
    ipAddr = 'localhost'
    server_address = (ipAddr, 10000)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)
    #print 'dsafsafsa'
    sock.listen(1)
    
    #print 'dsfsafdsafdsa'
    while True: #this while true statement is just to reopen listening
        #print 'dsafdsafdsafsafdsafsa'
        
              
        try:
            #===== If there is a desired limit to amount of time spent waiting for inbound message, enable throw exception at this amount of time 
            #sock.settimeout(1)
            #===== Wait for a connection to be made, and message sent.            
            print >>sys.stderr, 'waiting for a connection'    
            connection, client_address = sock.accept()
            #print ' -connection accepted-'
            complete_message=''
            print >>sys.stderr, 'connection from', client_address  
            
            #===== Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(32)
                print >>sys.stderr, 'received "%s"' % data
                if data:
                    print >>sys.stderr, 'sending data back to the client'
                    connection.sendall(data)
                    complete_message+=data
                else:
                    print >>sys.stderr, 'no more data from', client_address
                    break
            #====== Clean up the connection
            #print'Clean up connection -conn.close'
            connection.close()
        except socket.timeout:
            pass
            #this will only be thrown if a timeout value is set.
            #otherwise code will stop at input_socket.accept() until a connection is made
            #print 'socket timed out. could not find a connection to accept messages from.'                       
        #======
        # at this point complete_message now has full contents
        #======
            
        #evaluate contents of message
            #
            #if shutdown message received from client, break while loop        
        if 'exit-in' in complete_message:    
            break
    pass


if __name__ == '__main__':
    socket_in_v2()
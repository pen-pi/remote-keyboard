# first of all import the socket library 
import socket                
s = socket.socket()          
print "Socket successfully created"
port = 20000                
s.bind(('', port))         
print "socket binded to %s" %(port) 
s.listen(5)
print "socket is listening"            

def waitConnections(): 
   global s
   c, addr = s.accept()      
   print 'Got connection from', addr 
   incoming = c.recv(1024)
   while(incoming):
      c.send('Thank you for connecting') 
      print incoming
      incoming = c.recv(1024)
   c.close() 

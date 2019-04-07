from Tkinter import *
import socket # for socket 
import sys  

try: 
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
   print "Socket successfully created"
except socket.error as err: 
   print "socket creation failed with error %s" %(err) 
  
# default port for socket 
port = 20000
  
try: 
   host_ip = socket.gethostbyname('raspberrypi.local') 
except socket.gaierror: 
   # print "there was an error resolving the host"
   # sys.exit() 
   host_ip = "127.0.0.1"

root = Tk()
# connecting to the server 
s.connect((host_ip, port)) 
print "the socket has successfully connected to %s" %(host_ip) 

ctrl = False
shift = False
alt = False

def modifiers():
   global ctrl, alt, shift
   mod = ""
   if ctrl:
      mod = mod + "CONTROL "
   if shift:
      mod = mod + "SHIFT "
   if alt:
      mod = mod + "ALT "
   return mod


def key(event):
   global ctrl, alt, shift
   try:
      print "pressed",repr(event.char), repr(ord(event.char)),repr(event.keysym) # test what kind

      message = ""
      if(event.keysym == "Tab"):
         message = "TAB"
      else:
         message = event.char

      if ctrl or shift or alt:
         s.send(modifiers() +event.keysym)
         ctrl = False
         shift = False
         alt = False
      else:
         if message == " ":
            message = "SPACE"
            s.send(message)
         elif message == "\r":
            message = "ENTER"
            s.send(message)
         else:
            s.send("STRING " + message)
   except:
      print "pressed",repr(event.char),repr(event.keysym)
      message = ""
      onlyModifier= False
      if("Control" in event.keysym):
         ctrl = ctrl ^ True #toggle
         onlyModifier= True
      elif("Shift" in event.keysym):
         shift = shift ^ True #toggle
         onlyModifier= True
      elif("Alt" in event.keysym):
         alt = alt ^ True #toggle
         onlyModifier= True
      elif("Caps_Lock" in event.keysym):
         message = "CAPSLOCK"
      elif("Prior" in event.keysym):
         message = "PAGEUP"
      elif("Next" in event.keysym):
         message = "PAGEDOWN"
      # elif("" in event.keysym):
      #    message = ""
      else:
         message = event.keysym.upper()

      if message != "":
         s.send(modifiers() + message)
         ctrl = False
         shift = False
         alt = False



def callback(event):
    frame.focus_set()
    print "clicked at", event.x, event.y

frame = Frame(root, width=100, height=100)
frame.bind("<Key>", key)
frame.bind("<Button-1>", callback)
frame.pack()

root.mainloop()



  

  


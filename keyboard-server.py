#!/usr/bin/env python2

import sys
from Scancodes import *  
import time 
import struct
import socket                

 
class HIDReport:
   # https://gist.github.com/rmed/0d11b7225b3b772bb0dd89108ee93df0
   # http://www.freebsddiary.org/APC/usb_hid_usages.php

   def __init__():
      pass
   def setShift():
      pass
   def setCTRL():
      pass

def stringToReport():
   pass
   

def createReport():
   pass

def stringToReport(string, dev):
   for char in string:
      if char == '\n':
         continue
      if char in shiftedLetters:
         dev.write((chr(SHIFT)+NULL_CHAR+scancodes[char]+NULL_CHAR*5).encode())

      else: # if not shifted then do normal
         # print("not shifted", char)
         dev.write((NULL_CHAR*2+scancodes[char]+NULL_CHAR*5).encode())
      dev.write((NULL_CHAR*8).encode())

# def keyCombo(string):
#    with open('/dev/hidg0', 'rb+') as fd:
#       #fd.write(report.encode())
#       for char in string:
#          if char == '\n':
#             continue
#          if char in shiftedLetters:
#             fd.write((SHIFT+NULL_CHAR+scancodes[char]+NULL_CHAR*5).encode())

#          else:
#             fd.write((NULL_CHAR*2+scancodes[char]+NULL_CHAR*5).encode())
#          fd.write((NULL_CHAR*8).encode())
#       fd.close()


def displayHelp():
   print("Ducky Encoder for PenPi using Python 2.7")
   print("")
   print("Usage:")
   print("      ./ducky-encoder.py <ducky script> [test]")
   print("")
   print("Options:")
   #print("")
   print("  test          Use test to verify the script will run on the target platform. It will write to the file ./.deviceEmulated instead of the emulated HID keyboard.")



def isInt(s):
   try: 
      int(s)
      return True
   except ValueError:
      return False



def processLine(line, dev, modifiers = NULL_MODIFIER):
   toks = line.split(None, 1)
   if len(toks) >= 2:
      command, arguments = toks
      if arguments[len(arguments)-1] == '\n':
         arguments = arguments[0:len(arguments)-1] # removing the \n at the end
   else:
      command = toks[0]
      arguments = ''

   if command == "REM":
      print "Comment: ", arguments

   elif command == "DEFAULT_DELAY" or command == "DEFAULTDELAY":
      if isInt(arguments):
         # TODO set default delay to int
         #print("TODO: set default value to "+arguments)
         if int(arguments) >= 0:
            loop_delay = int(arguments)
      else:
         sys.exit("Error line "+str(lineNUmb)+": argument of DEFAULT_DELAY has to be integer")

   elif command == "DELAY":
      #print("DELAY")
      if isInt(arguments):

         time.sleep(int(arguments)/1000.0)
      else:
         return False

   elif command == "STRING":
      stringToReport(arguments,dev)

   elif command == "WINDOWS" or command == "GUI":
      argLen = len(arguments) 
      if argLen >= 2:
         sys.exit("Error in line "+str(lineNUmb)+". GUI can only have one CHAR as argument.")
      elif argLen == 0:
         dev.write((chr(GUI | modifiers)+NULL_CHAR+NULL_CHAR*6).encode())
      elif argLen == 1:
         # print(("val", arguments))
         # print(type(int(GUI)))
         dev.write((chr(GUI | modifiers)+NULL_CHAR+scancodes[arguments]+NULL_CHAR*5).encode())
      else:
         return False

   elif command == "MENU" or command == "APP":
      dev.write((modifiers+NULL_CHAR+scancodes["APP"]+NULL_CHAR*5).encode())
      
   elif command == "SHIFT":
      argLen = len(arguments)
      if argLen == 0:
         dev.write((chr(SHIFT | modifiers)+NULL_CHAR+NULL_CHAR*6).encode())
      elif argLen ==1:
         dev.write((chr(SHIFT | modifiers)+NULL_CHAR+scancodes[arguments]+NULL_CHAR*5).encode())
      else:
         processLine(arguments, dev, modifiers | SHIFT)

   elif command == "ALT":
      argLen = len(arguments)
      if argLen == 0:
         print("0", arguments)
         dev.write((chr(ALT | modifiers)+NULL_CHAR+NULL_CHAR*6).encode())
      elif argLen ==1:
         print("1", arguments)
         dev.write((chr(ALT | modifiers)+NULL_CHAR+scancodes[arguments]+NULL_CHAR*5).encode())
      else:
         print("difering", arguments)
         processLine(arguments, dev, modifiers | ALT)

   elif command == "CONTROL" or command == "CTRL":
      argLen = len(arguments)
      if argLen == 0:
         dev.write((chr(CTRL | modifiers)+NULL_CHAR+NULL_CHAR*6).encode())
      elif argLen ==1:
         dev.write((chr(CTRL | modifiers)+NULL_CHAR+scancodes[arguments]+NULL_CHAR*5).encode())
      else:
         processLine(arguments, dev, modifiers | CTRL)

   elif command == "DOWNARROW" or command == "DOWN":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["DOWN"]+NULL_CHAR*5).encode())

   elif command == "LEFTARROW" or command == "LEFT":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["LEFT"]+NULL_CHAR*5).encode())
   elif command == "RIGHTARROW" or command == "RIGHT":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["RIGHT"]+NULL_CHAR*5).encode())
   elif command == "UPARROW" or command == "UP":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["UP"]+NULL_CHAR*5).encode())

   elif command == "BREAK" or command == "PAUSE":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["PAUSE"]+NULL_CHAR*5).encode())

   elif command == "CAPSLOCK":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["CAPSLOCK"]+NULL_CHAR*5).encode())

   elif command == "DELETE":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["DELETE"]+NULL_CHAR*5).encode())

   elif command == "END":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["END"]+NULL_CHAR*5).encode())

   elif command == "ESC" or command == "ESCAPE":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["ESCAPE"]+NULL_CHAR*5).encode())

   elif command == "HOME":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["HOME"]+NULL_CHAR*5).encode())

   elif command == "INSERT":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["INSERT"]+NULL_CHAR*5).encode())

   elif command == "NUMLOCK":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["NUMLOCK"]+NULL_CHAR*5).encode())

   elif command == "PAGEUP":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["PAGEUP"]+NULL_CHAR*5).encode())

   elif command == "PAGEDOWN":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["PAGEDOWN"]+NULL_CHAR*5).encode())

   elif command == "PRINTSCREEN":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["PRINTSCREEN"]+NULL_CHAR*5).encode())

   elif command == "SCROLLLOCK":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["SCROLLLOCK"]+NULL_CHAR*5).encode())

   elif command == "SPACE":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["SPACE"]+NULL_CHAR*5).encode())

   elif command == "TAB":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["TAB"]+NULL_CHAR*5).encode())

   elif command == "ENTER":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["ENTER"]+NULL_CHAR*5).encode())
   
   elif command == "F1":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["F1"]+NULL_CHAR*5).encode())
   elif command == "F2":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["F2"]+NULL_CHAR*5).encode())
   elif command == "F3":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["F3"]+NULL_CHAR*5).encode())
   elif command == "F4":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["F4"]+NULL_CHAR*5).encode())
   elif command == "F5":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["F5"]+NULL_CHAR*5).encode())
   elif command == "F6":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["F6"]+NULL_CHAR*5).encode())
   elif command == "F7":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["F7"]+NULL_CHAR*5).encode())
   elif command == "F8":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["F8"]+NULL_CHAR*5).encode())
   elif command == "F9":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["F9"]+NULL_CHAR*5).encode())
   elif command == "F10":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["F10"]+NULL_CHAR*5).encode())
   elif command == "F11":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["F11"]+NULL_CHAR*5).encode())
   elif command == "F12":
      dev.write((chr(modifiers)+NULL_CHAR+scancodes["F12"]+NULL_CHAR*5).encode())

   else:
      #print command
      return False
   return True



def waitConnectionsAndRun(): 
   global s, device
   c, addr = s.accept()      
   print 'Got connection from', addr 
   incoming = c.recv(1024)
   while(incoming):
      #c.send('Thank you for connecting') 
      print incoming
      try:
         device = open(devLocation, 'rb+')
         processLine(incoming, device):
         device.write((NULL_CHAR*8).encode())
         device.close()
      except:
         sys.exit("Error: Can not open "+devLocation)
      incoming = c.recv(1024)
   c.close() 

################################################################
########################### MAIN ###############################
################################################################



s = socket.socket()          
print "Socket successfully created"
port = 20000                
s.bind(('', port))         
print "socket binded to %s" %(port) 
s.listen(5)
print "socket is listening" 


waitConnectionsAndRun()


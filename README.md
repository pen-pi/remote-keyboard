# Remote Keyboard
Fork of the `ducky-encoder` project by PenPi.   

Converts ducky script to HID via a socket connection.     
One tcp per one ducky script line.  
It fully implements all the protocol.   

It implements the HID Boot protocol as specified by the following:   
https://www.usb.org/sites/default/files/documents/hid1_11.pdf   
https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf   
https://wiki.osdev.org/USB_Human_Interface_Devices   


# Scancodes
** IMPORTANT **
Scancodes are not included in this repo. Please retrieve from the `ducky-encoder` project by PenPi and add to the same directory as this.
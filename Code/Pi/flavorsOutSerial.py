import parms
import time

def sendFlavorValues():
  parms.ser.write(b'Blink\n')  # Send a message

import parms
import time

def sendFlavorValues():
  parms.ser.write(b'Blink\n')  # Send a message
  print("Sent: Blink")
  time.sleep(2)  # Wait before sending again

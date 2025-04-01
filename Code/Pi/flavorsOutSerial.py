import parms
import time

def sendFlavorValues():
  data = f"{parms.currentDrink.flavor1Perc},{parms.currentDrink.flavor2Perc},{parms.currentDrink.flavor3Perc},{parms.currentDrink.flavor4Perc},{parms.currentDrink.carbPerc}\n"
  parms.ser.write(data.encode())  # Send a message 

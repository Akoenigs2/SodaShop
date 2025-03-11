import parms
import serial

def sendFlavorValues():
  with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
    values = [parms.currentDrink.flavor1Perc, parms.currentDrink.flavor2Perc, parms.currentDrink.flavor3Perc, parms.currentDrink.flavor4Perc, parms.currentDrink.carbPerc]  # Example integer values
    data = ",".join(map(str, values)) + "\n"  # Format as CSV string
    parms.ser.write(data.encode())  # Send data
    print(f"Sent: {data.strip()}")

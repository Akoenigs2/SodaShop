import parms
import serial
from guizero import App

def sendFlavorValues():
  popup = parms.app.yesno("Confirm Dispense", "Are you sure you want to dispense this drink?")
  if (popup == False):
    return

  SERIAL_PORT = '/dev/ttyACM0'
  BAUD_RATE = 115200
  p1 = parms.currentDrink['value'].flavor1Perc
  p2 = parms.currentDrink['value'].flavor2Perc
  p3 = parms.currentDrink['value'].flavor3Perc
  p4 = parms.currentDrink['value'].flavor4Perc
  p5 = parms.currentDrink['value'].carbPerc

  try:
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
      data = f"{p1},{p2},{p3},{p4},{p5}\n"
      ser.write(data.encode('utf-8'))
      print(f"Sent: {data.strip()}")
  except serial.SerialException as e:
    print("Serial error:", e)

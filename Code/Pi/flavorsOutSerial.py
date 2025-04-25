import parms
import serial
from guizero import App

def sendFlavorValues(selection):
  dispensingDrink = parms.currentDrink['value']
  if selection != "custom":
    dispensingDrink = parms.favoriteDrinks[int(selection)]

  popup = parms.app.yesno("Confirm Dispense", "Are you sure you want to dispense " + dispensingDrink.name + "?")
  if (popup == False):
    return

  # TODO: Uncomment when on Pi
  # SERIAL_PORT = '/dev/ttyACM0'
  # BAUD_RATE = 115200
  # p1 = dispensingDrink.flavor1Perc
  # p2 = dispensingDrink.flavor2Perc
  # p3 = dispensingDrink.flavor3Perc
  # p4 = dispensingDrink.flavor4Perc
  # p5 = dispensingDrink.carbPerc

  # try:
  #   with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
  #     data = f"{p1},{p2},{p3},{p4},{p5}\n"
  #     ser.write(data.encode('utf-8'))
  #     print(f"Sent: {data.strip()}")
  # except serial.SerialException as e:
  #   print("Serial error:", e)

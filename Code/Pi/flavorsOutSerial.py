import parms
import serial
from guizero import App

def sendFlavorValues(selection):
  def mapFlavorValues():
    dispensingDrinkFlavors = [dispensingDrink.flavor1Name, dispensingDrink.flavor2Name, dispensingDrink.flavor3Name, dispensingDrink.flavor4Name]
    chosenFlavorNames = parms.getListOfChosenFlavorNames()
    for i, drinkFlavor in enumerate(dispensingDrinkFlavors):
      for j, selectedFlavor in enumerate(chosenFlavorNames):
        if drinkFlavor == selectedFlavor:
          if j == 1:
            if (i == 1):
              p1 = dispensingDrink.flavor1Perc
            elif (i == 2):
              p1 = dispensingDrink.flavor2Perc
            elif (i == 3):
              p1 = dispensingDrink.flavor3Perc
            elif (i == 4):
              p1 = dispensingDrink.flavor4Perc
          elif j == 2:
            if (i == 1):
              p2 = dispensingDrink.flavor1Perc
            elif (i == 2):
              p2 = dispensingDrink.flavor2Perc
            elif (i == 3):
              p2 = dispensingDrink.flavor3Perc
            elif (i == 4):
              p2 = dispensingDrink.flavor4Perc
          elif j == 3:
            if (i == 1):
              p3 = dispensingDrink.flavor1Perc
            elif (i == 2):
              p3 = dispensingDrink.flavor2Perc
            elif (i == 3):
              p3 = dispensingDrink.flavor3Perc
            elif (i == 4):
              p3 = dispensingDrink.flavor4Perc
          elif j == 4:
            if (i == 1):
              p4 = dispensingDrink.flavor1Perc
            elif (i == 2):
              p4 = dispensingDrink.flavor2Perc
            elif (i == 3):
              p4 = dispensingDrink.flavor3Perc
            elif (i == 4):
              p4 = dispensingDrink.flavor4Perc

  dispensingDrink = parms.currentDrink['value']
  if selection != "custom":
    dispensingDrink = parms.favoriteDrinks[int(selection)]

  popup = parms.app.yesno("Confirm Dispense", "Are you sure you want to dispense " + dispensingDrink.name + "?")
  if (popup == False):
    return

  p1 = 0
  p2 = 0
  p3 = 0
  p4 = 0
  p5 = 0

  mapFlavorValues()
  
  # TODO: Uncomment when on Pi
  SERIAL_PORT = '/dev/ttyACM0'
  BAUD_RATE = 115200

  try:
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
      data = f"{p1},{p2},{p3},{p4},{p5}\n"
      ser.write(data.encode('utf-8'))
      print(f"Sent: {data.strip()}")
  except serial.SerialException as e:
    print("Serial error:", e)

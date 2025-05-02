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

  p = [0, 0, 0, 0, dispensingDrink.carbPerc]

  dispensingDrinkFlavors = [dispensingDrink.flavor1Name, dispensingDrink.flavor2Name, dispensingDrink.flavor3Name, dispensingDrink.flavor4Name]
    
  chosenFlavorNames = parms.getListOfChosenFlavorNames()
  for i, drinkFlavor in enumerate(dispensingDrinkFlavors):
    for j, selectedFlavor in enumerate(chosenFlavorNames):
      if drinkFlavor == selectedFlavor:
        print (drinkFlavor)
        print (selectedFlavor)
        print (dispensingDrink.flavor1Perc)
        print(i, j)
        if j == 0:
          if (i == 0):
            p[0] = dispensingDrink.flavor1Perc
          elif (i == 1):
            p[0] = dispensingDrink.flavor2Perc
          elif (i == 2):
            p[0] = dispensingDrink.flavor3Perc
          elif (i == 3):
            p[0] = dispensingDrink.flavor4Perc
        elif j == 1:
          if (i == 0):
            p[1] = dispensingDrink.flavor1Perc
          elif (i == 1):
            p[1] = dispensingDrink.flavor2Perc
          elif (i == 2):
            p[1] = dispensingDrink.flavor3Perc
          elif (i == 3):
            p[1] = dispensingDrink.flavor4Perc
        elif j == 2:
          if (i == 0):
            p[2] = dispensingDrink.flavor1Perc
          elif (i == 1):
            p[2] = dispensingDrink.flavor2Perc
          elif (i == 2):
            p[2] = dispensingDrink.flavor3Perc
          elif (i == 3):
            p[2] = dispensingDrink.flavor4Perc
        elif j == 3:
          if (i == 0):
            p[3] = dispensingDrink.flavor1Perc
          elif (i == 1):
            p[3] = dispensingDrink.flavor2Perc
          elif (i == 2):
            p[3] = dispensingDrink.flavor3Perc
          elif (i == 3):
            p[3] = dispensingDrink.flavor4Perc
  
  print(p[0], p[1], p[2], p[3], p[4])

  # TODO: Uncomment when on Pi
  SERIAL_PORT = '/dev/ttyACM0'
  BAUD_RATE = 115200

  try:
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
      data = f"{p[0]},{p[1]},{p[2]},{p[3]},{p[4]}\n"
      ser.write(data.encode('utf-8'))
      print(f"Sent: {data.strip()}")
  except serial.SerialException as e:
    print("Serial error:", e)

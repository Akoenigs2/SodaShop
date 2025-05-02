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

  p1 = {'value':0}
  p2 = {'value':0}
  p3 = {'value':0}
  p4 = {'value':0}
  p5 = {'value':0}

  dispensingDrinkFlavors = [dispensingDrink.flavor1Name, dispensingDrink.flavor2Name, dispensingDrink.flavor3Name, dispensingDrink.flavor4Name]
    
  chosenFlavorNames = parms.getListOfChosenFlavorNames()
  for i, drinkFlavor in enumerate(dispensingDrinkFlavors):
    for j, selectedFlavor in enumerate(chosenFlavorNames):
      if drinkFlavor == selectedFlavor:
        if j == 1:
          if (i == 1):
            parms.modify_value(p1, dispensingDrink.flavor1Perc)
          elif (i == 2):
            parms.modify_value(p1, dispensingDrink.flavor2Perc)
          elif (i == 3):
            parms.modify_value(p1, dispensingDrink.flavor3Perc)
          elif (i == 4):
            parms.modify_value(p1, dispensingDrink.flavor4Perc)
        elif j == 2:
          if (i == 1):
            parms.modify_value(p2, dispensingDrink.flavor1Perc)
          elif (i == 2):
            parms.modify_value(p2, dispensingDrink.flavor2Perc)
          elif (i == 3):
            parms.modify_value(p2, dispensingDrink.flavor3Perc)
          elif (i == 4):
            parms.modify_value(p2, dispensingDrink.flavor4Perc)
        elif j == 3:
          if (i == 1):
            parms.modify_value(p3, dispensingDrink.flavor1Perc)
          elif (i == 2):
            parms.modify_value(p3, dispensingDrink.flavor2Perc)
          elif (i == 3):
            parms.modify_value(p3, dispensingDrink.flavor3Perc)
          elif (i == 4):
            parms.modify_value(p3, dispensingDrink.flavor4Perc)
        elif j == 4:
          if (i == 1):
            parms.modify_value(p4, dispensingDrink.flavor1Perc)
          elif (i == 2):
            parms.modify_value(p4, dispensingDrink.flavor2Perc)
          elif (i == 3):
            parms.modify_value(p4, dispensingDrink.flavor3Perc)
          elif (i == 4):
            parms.modify_value(p4, dispensingDrink.flavor4Perc)
  
  # TODO: Uncomment when on Pi
  SERIAL_PORT = '/dev/ttyACM0'
  BAUD_RATE = 115200

  try:
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
      data = f"{p1['value']},{p2['value']},{p3['value']},{p4['value']},{p5['value']}\n"
      ser.write(data.encode('utf-8'))
      print(f"Sent: {data.strip()}")
  except serial.SerialException as e:
    print("Serial error:", e)

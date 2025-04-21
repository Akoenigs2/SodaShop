import parms
import drinkMenu
import flavorsOutSerial
import flavorMenu
from guizero import Box, ListBox, PushButton

# Select Drink Function
def selectDrink(selection):
  for drink in parms.drinks:
    if (selection == drink.name):
      parms.modify_value(parms.currentDrink, drink)
      break
  # Load Selected Drink
  if (not selection == None):
    if (parms.validDrinkSelection['value']):
      dispenseButton.text = "Dispense: " + parms.currentDrink['value'].name + "\n"
    else:
      dispenseButton.text = "Not correct flavors, please load: "
      if (not parms.currentDrink['value'].flavor1Name in parms.chosenFlavors) and (parms.currentDrink['value'].flavor1Perc > 0) and (not parms.currentDrink['value'].flavor1Name == "None"):
        dispenseButton.text += parms.currentDrink['value'].flavor1Name + ", "
      if (not parms.currentDrink['value'].flavor2Name in parms.chosenFlavors) and (parms.currentDrink['value'].flavor2Perc > 0) and (not parms.currentDrink['value'].flavor2Name == "None"):
        dispenseButton.text += parms.currentDrink['value'].flavor2Name + ", "
      if (not parms.currentDrink['value'].flavor3Name in parms.chosenFlavors) and (parms.currentDrink['value'].flavor3Perc > 0) and (not parms.currentDrink['value'].flavor3Name == "None"):
        dispenseButton.text += parms.currentDrink['value'].flavor3Name + ", "
      if (not parms.currentDrink['value'].flavor4Name in parms.chosenFlavors) and (parms.currentDrink['value'].flavor4Perc > 0) and (not parms.currentDrink['value'].flavor4Name == "None"):
        dispenseButton.text += parms.currentDrink['value'].flavor4Name + ", "
      dispenseButton.text = dispenseButton.text[:-2] + "\n"
  
    dispenseButton.text += "Needed Flavors: "
    if (parms.currentDrink['value'].flavor1Perc > 0) and (not parms.currentDrink['value'].flavor1Name == "None"):
      dispenseButton.text += parms.currentDrink['value'].flavor1Name + ", "
    if (parms.currentDrink['value'].flavor2Perc > 0) and (not parms.currentDrink['value'].flavor2Name == "None"):
      dispenseButton.text += parms.currentDrink['value'].flavor2Name + ", "
    if (parms.currentDrink['value'].flavor3Perc > 0) and (not parms.currentDrink['value'].flavor3Name == "None"):
      dispenseButton.text += parms.currentDrink['value'].flavor3Name + ", "
    if (parms.currentDrink['value'].flavor4Perc > 0) and (not parms.currentDrink['value'].flavor4Name == "None"):
      dispenseButton.text += parms.currentDrink['value'].flavor4Name + ", "
    dispenseButton.text = dispenseButton.text[:-2]

def selectInvalidDrink(selection):
  parms.modify_value(parms.validDrinkSelection, False)
  selectDrink(selection)

def selectionValidDrink(selection):
  parms.modify_value(parms.validDrinkSelection, True)
  selectDrink(selection)

def createNewDrink():
    parms.modify_value(parms.newDrinkFlag, True)
    drinkMenu.editDrink()

def clearLists():
  invalidDrinkList.clear()
  validDrinkList.clear()
  
def updateDrinkNameLists():
  parms.drinkNames.clear()
  parms.invalidDrinkNames.clear()
  clearLists()
  for drink in parms.drinks:
      if ((drink.flavor1Perc > 0) and (not drink.flavor1Name in parms.chosenFlavors) and (not drink.flavor1Name == "None")):
        parms.invalidDrinkNames.append(drink.name)
        invalidDrinkList.append(drink.name)
      elif ((drink.flavor2Perc > 0) and (not drink.flavor2Name in parms.chosenFlavors) and (not drink.flavor2Name == "None")):
        parms.invalidDrinkNames.append(drink.name)
        invalidDrinkList.append(drink.name)
      elif ((drink.flavor3Perc > 0) and (not drink.flavor3Name in parms.chosenFlavors) and (not drink.flavor3Name == "None")):
        parms.invalidDrinkNames.append(drink.name)
        invalidDrinkList.append(drink.name)
      elif ((drink.flavor4Perc > 0) and (not drink.flavor4Name in parms.chosenFlavors) and (not drink.flavor4Name == "None")):
        parms.invalidDrinkNames.append(drink.name)
        invalidDrinkList.append(drink.name)
      else:
        parms.drinkNames.append(drink.name)
        validDrinkList.append(drink.name)

def home():
    # Make widgets global
    global validDrinkList
    global invalidDrinkList
    global flavor1Button
    global flavor2Button
    global flavor3Button
    global flavor4Button
    global dispenseButton

    # Main menu logic
    drinkListBox = Box(parms.app, height="fill", align="right")
    validDrinkList = ListBox(drinkListBox, items=parms.drinkNames, height="fill", align="top", command=selectionValidDrink, scrollbar=True)
    invalidDrinkList = ListBox(drinkListBox, items=parms.invalidDrinkNames, height="fill", align="bottom", command=selectInvalidDrink, scrollbar = True)
    invalidDrinkList.bg = "#e0dcdc"

    updateDrinkNameLists()

    flavorsSettingsBox = Box(parms.app, width="fill", align="top", border=True)
    flavor1Button = PushButton(flavorsSettingsBox, text=parms.chosenFlavors[0], align="left", command=flavorMenu.editFlavor, args="0")
    flavor1Button.bg = parms.chosenFlavorsColors[0]
    flavor2Button = PushButton(flavorsSettingsBox, text=parms.chosenFlavors[1], align="left", command=flavorMenu.editFlavor, args="1")
    flavor2Button.bg = parms.chosenFlavorsColors[1]
    flavor3Button = PushButton(flavorsSettingsBox, text=parms.chosenFlavors[2], align="left", command=flavorMenu.editFlavor, args="2")
    flavor3Button.bg = parms.chosenFlavorsColors[2]
    flavor4Button = PushButton(flavorsSettingsBox, text=parms.chosenFlavors[3], align="left", command=flavorMenu.editFlavor, args="3")
    flavor4Button.bg = parms.chosenFlavorsColors[3]

    editDrinkButton = PushButton(flavorsSettingsBox, text="Edit Selected Drink", align="right", command=drinkMenu.editDrink)
    createNewDrinkButton = PushButton(flavorsSettingsBox, text=parms.editDrinkText, align="right", command=createNewDrink)
    dispenseButton = PushButton(parms.app, text="Select a Drink", width="fill", height="fill", command=flavorsOutSerial.sendFlavorValues)

import parms
import drinkMenu
import flavorsOutSerial
import flavorMenu
import favoriteMenu
import settings
from guizero import Box, ListBox, PushButton, Combo

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
  parms.validDrinks.clear()
  parms.invalidDrinks.clear()
  clearLists()
  chosenFlavorNames = []
  for chosenFlavor in parms.chosenFlavors:
    chosenFlavorNames.append(chosenFlavor.name)
  for drink in parms.drinks:
      if ((drink.flavor1Perc > 0) and (not (drink.flavor1Name in chosenFlavorNames)) and (not drink.flavor1Name == "None")):
        parms.invalidDrinks.append(drink)
      elif ((drink.flavor2Perc > 0) and (not drink.flavor2Name in chosenFlavorNames) and (not drink.flavor2Name == "None")):
        parms.invalidDrinks.append(drink)
      elif ((drink.flavor3Perc > 0) and (not drink.flavor3Name in chosenFlavorNames) and (not drink.flavor3Name == "None")):
        parms.invalidDrinks.append(drink)
      elif ((drink.flavor4Perc > 0) and (not drink.flavor4Name in chosenFlavorNames) and (not drink.flavor4Name == "None")):
        parms.invalidDrinks.append(drink)
      else:
        parms.validDrinks.append(drink)
  for validDrink in parms.validDrinks:
    validDrinkList.append(validDrink.name)
  for invalidDrink in parms.invalidDrinks:
    invalidDrinkList.append(invalidDrink.name)

def setFlavorColor1():
  parms.chosenFlavors[0] = parms.findFlavorFromName(flavor1Button.value)
  flavor1Button.bg = parms.chosenFlavors[0].color
  updateDrinkNameLists()
  settings.saveSettings()
def setFlavorColor2():
  parms.chosenFlavors[1] = parms.findFlavorFromName(flavor2Button.value)
  flavor2Button.bg = parms.chosenFlavors[1].color
  updateDrinkNameLists()
  settings.saveSettings()
def setFlavorColor3():
  parms.chosenFlavors[2] = parms.findFlavorFromName(flavor3Button.value)
  flavor3Button.bg = parms.chosenFlavors[2].color
  updateDrinkNameLists()
  settings.saveSettings()
def setFlavorColor4():
  parms.chosenFlavors[3] = parms.findFlavorFromName(flavor4Button.value)
  flavor4Button.bg = parms.chosenFlavors[3].color
  updateDrinkNameLists()
  settings.saveSettings()

def updateFlavorColors():
  setFlavorColor1()
  setFlavorColor2()
  setFlavorColor3()
  setFlavorColor4()

def updateFlavorButtons():
  flavor1Button.clear()
  flavor2Button.clear()
  flavor3Button.clear()
  flavor4Button.clear()
  flavor1Button.append(parms.getListofFlavorNames())
  flavor2Button.append(parms.getListofFlavorNames())
  flavor3Button.append(parms.getListofFlavorNames())
  flavor4Button.append(parms.getListofFlavorNames())

def updateFavoriteButtons():
  for i in range(len(parms.favoriteDrinks)):
    favoriteDrinkButtons[i].bg = parms.favoriteDrinks[i].color
    favoriteDrinkButtons[i].text = parms.favoriteDrinks[i].name

def home():
    # Make widgets global
    global validDrinkList
    global invalidDrinkList
    global flavor1Button
    global flavor2Button
    global flavor3Button
    global flavor4Button
    global dispenseButton
    global favoriteDrinkButtons

    # Main menu logic
    
    drinkListBox = Box(parms.app, height="fill", align="right")
    validDrinkList = ListBox(drinkListBox, items=parms.getListOfValidDrinksNames(), height="fill", align="top", command=selectionValidDrink, scrollbar=True)
    invalidDrinkList = ListBox(drinkListBox, items=parms.getListOfInvalidDrinksNames(), height="fill", align="bottom", command=selectInvalidDrink, scrollbar = True)
    invalidDrinkList.bg = "#e0dcdc"

    updateDrinkNameLists()

    flavorsSettingsBox = Box(parms.app, width="fill", align="top", border=True)
    flavor1Button = Combo(flavorsSettingsBox, options=parms.getListOfFlavorNames(), selected=parms.chosenFlavors[0].name, align="left", command=setFlavorColor1)
    flavor1Button.bg = parms.chosenFlavors[0].color
    flavor2Button = Combo(flavorsSettingsBox, options=parms.getListOfFlavorNames(), selected=parms.chosenFlavors[1].name, align="left", command=setFlavorColor2)
    flavor2Button.bg = parms.chosenFlavors[1].color
    flavor3Button = Combo(flavorsSettingsBox, options=parms.getListOfFlavorNames(), selected=parms.chosenFlavors[2].name, align="left", command=setFlavorColor3)
    flavor3Button.bg = parms.chosenFlavors[2].color
    flavor4Button = Combo(flavorsSettingsBox, options=parms.getListOfFlavorNames(), selected=parms.chosenFlavors[3].name, align="left", command=setFlavorColor4)
    flavor4Button.bg = parms.chosenFlavors[3].color

    editFlavors = PushButton(flavorsSettingsBox, text="Edit Flavors", align="right", command=flavorMenu.editFlavor)
    editFavoriteDrinks = PushButton(flavorsSettingsBox, text="Edit Favorite Drinks", align="right", command=favoriteMenu.editFavorites)
    editDrinkButton = PushButton(flavorsSettingsBox, text="Edit Selected Drink", align="right", command=drinkMenu.editDrink)
    createNewDrinkButton = PushButton(flavorsSettingsBox, text="Create New Drink", align="right", command=createNewDrink)
    
    favoriteDrinkButtons = []
    for i in range(len(parms.favoriteDrinks)):
      favoriteButton = PushButton(parms.app, text=parms.favoriteDrinks[i].name, width="fill", height="fill", command=flavorsOutSerial.sendFlavorValues, args=str(i))
      favoriteButton.bg = parms.favoriteDrinks[i].color
      favoriteDrinkButtons.append(favoriteButton)

    dispenseButton = PushButton(parms.app, text="Select a Drink", width="fill", height="fill", command=flavorsOutSerial.sendFlavorValues, args=["custom"])

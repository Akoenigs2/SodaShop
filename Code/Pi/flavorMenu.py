import parms
import settings
import homeMenu
from guizero import Window, Box, PushButton, ListBox

# Edit Flavor Menu
def editFlavor(selection):
  def saveAndCloseWindow():
    import homeMenu
    if (selection == "0"):
      parms.chosenFlavors[0] = parms.flavors[currentFlavorIndex['value']]
      parms.chosenFlavorsColors[0] = parms.flavorColors[currentFlavorIndex['value']]
      homeMenu.flavor1Button.text = parms.flavors[currentFlavorIndex['value']]
      homeMenu.flavor1Button.bg = parms.flavorColors[currentFlavorIndex['value']]
    elif (selection == "1"):
      parms.chosenFlavors[1] = parms.flavors[currentFlavorIndex['value']]
      parms.chosenFlavorsColors[1] = parms.flavorColors[currentFlavorIndex['value']]
      homeMenu.flavor2Button.text = parms.flavors[currentFlavorIndex['value']]
      homeMenu.flavor2Button.bg = parms.flavorColors[currentFlavorIndex['value']]
    elif (selection == "2"):
      parms.chosenFlavors[2] = parms.flavors[currentFlavorIndex['value']]
      parms.chosenFlavorsColors[2] = parms.flavorColors[currentFlavorIndex['value']]
      homeMenu.flavor3Button.text = parms.flavors[currentFlavorIndex['value']]
      homeMenu.flavor3Button.bg = parms.flavorColors[currentFlavorIndex['value']]
    elif (selection == "3"):
      parms.chosenFlavors[3] = parms.flavors[currentFlavorIndex['value']]
      parms.chosenFlavorsColors[3] = parms.flavorColors[currentFlavorIndex['value']]
      homeMenu.flavor4Button.text = parms.flavors[currentFlavorIndex['value']]
      homeMenu.flavor4Button.bg = parms.flavorColors[currentFlavorIndex['value']]
    settings.saveSettings()
    homeMenu.updateDrinkNameLists()
    closeWindow()

  def closeWindow():
    flavorWindow.hide()
    flavorWindow.destroy()

  def createNewFlavor():
    flavorQuestion = flavorWindow.question("Flavor Edit", "Enter new flavor name")
    if (not flavorQuestion in parms.flavors):
      parms.flavors.append(flavorQuestion)
      parms.flavorColors.append("#ffffff")
      chooseFlavorList.append(flavorQuestion)
      settings.saveSettings()

  def chooseFlavor(flavor):
    parms.modify_value(currentFlavorIndex,parms.flavors.index(flavor))
    colorButton.show()
    colorButton.bg = parms.flavorColors[currentFlavorIndex['value']]
    saveButton.show()
    deleteButton.show()

  def selectColor():
    color = "None"
    color = flavorWindow.select_color(color=parms.flavorColors[currentFlavorIndex['value']])
    parms.flavorColors[currentFlavorIndex['value']] = color
    colorButton.bg = color
  
  def deleteFlavor():
    chooseFlavorList.remove(parms.flavors[currentFlavorIndex['value']])
    parms.flavors.pop(currentFlavorIndex['value'])
    parms.flavorColors.pop(currentFlavorIndex['value'])
    
  currentFlavorIndex = {'value':0}
  flavorWindow = Window(parms.app, title="Swap Flavor")
  flavorWindow.show(wait=True)
  flavorWindow.set_full_screen()
  settingsBox = Box(flavorWindow, width="fill", align="top")
  exitButton = PushButton(settingsBox, text="Back", command=closeWindow, align="left")
  saveButton = PushButton(settingsBox, text="Save", command=saveAndCloseWindow, align="right")
  saveButton.hide()
  newFlavorButton = PushButton(settingsBox, text="Create New Flavor", command=createNewFlavor, align="right")
  deleteButton = PushButton(settingsBox, text="Delete", align="left", command=deleteFlavor)
  deleteButton.hide()
  chooseFlavorList = ListBox(flavorWindow, items=parms.flavors, align="left", height="fill", command=chooseFlavor)
  colorButton = PushButton(flavorWindow, text="Color", width="fill", command=selectColor)
  colorButton.hide()

  settings.saveSettings()
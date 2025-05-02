import parms
import settings
import homeMenu
import subprocess
import os
from guizero import Window, Box, PushButton, ListBox, TextBox

# Edit Flavor Menu
def editFlavor():
  
  def show_keyboard(event=None):
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(["onboard"],env=env)

  def hide_keyboard(event=None):
    subprocess.Popen(["pkill","onboard"])

  def on_return(event=None):
    hide_keyboard()

  def saveAndCloseWindow():
    settings.saveSettings()
    homeMenu.updateDrinkNameLists()
    homeMenu.updateFlavorButtons()
    closeWindow()

  def closeWindow():
    flavorWindow.hide()
    flavorWindow.destroy()

  def createNewFlavor():
    show_keyboard()
    flavorQuestion = flavorWindow.question("Flavor Edit", "Enter new flavor name")
    hide_keyboard()
    if (not flavorQuestion in parms.flavors):
      parms.flavors.append(parms.Flavor(flavorQuestion, "#ffffff"))
      flavorsList.append(flavorQuestion)
      settings.saveSettings()

  def selectFlavor(selection):
    currentFlavor = selection
    chooseFlavor(True)

  def chooseFlavor(show):
    colorButton.show()
    colorButton.bg = next((flavor.color for flavor in parms.flavors if flavor.name == flavorsList.value), "#ffffff")
    saveButton.show()
    copyFlavorButton.show()
    deleteButton.show()
    if (show):
      colorButton.show()
      colorButton.bg = next((flavor.color for flavor in parms.flavors if flavor.name == flavorsList.value), "#ffffff")
      copyFlavorButton.show()
      deleteButton.show()
    else:
      colorButton.hide()
      copyFlavorButton.hide()
      deleteButton.hide()

  def selectColor():
    color = "None"
    color = flavorWindow.select_color(color=next((flavor.color for flavor in parms.flavors if flavor.name == flavorsList.value), "#ffffff"))
    if (color == None):
      color = "#ffffff"
    for i, flavor in enumerate(parms.flavors):
      if flavor.name == flavorsList.value:
        parms.flavors[i].color = color
    colorButton.bg = color
  
  def copyFlavor():
    selectedFlavor = parms.findFlavorFromName(flavorsList.value)
    parms.flavors.append(selectedFlavor)
    updateFlavorList()

  def deleteFlavor():
    for i, flavor in enumerate(parms.flavors):
      if parms.flavors[i].name == flavorsList.value:
        parms.flavors.pop(i)
        chooseFlavor(False)
        break
    for i, chosenFlavor in enumerate(parms.chosenFlavors):
      if parms.chosenFlavors[i].name == flavorsList.value:
        parms.chosenFlavors[i] = parms.Flavor("None", "#ffffff")
    updateFlavorList()
  
  def updateFlavorList():
    flavorsList.clear()
    for flavor in parms.flavors:
      flavorsList.append(flavor.name)

  flavorWindow = Window(parms.app, title="Edit Flavors")
  flavorWindow.show(wait=True)
  flavorWindow.set_full_screen()
  settingsBox = Box(flavorWindow, width="fill", align="top")
  saveButton = PushButton(settingsBox, text="Save", command=saveAndCloseWindow, align="right")
  newFlavorButton = PushButton(settingsBox, text="Create New Flavor", command=createNewFlavor, align="left")
  deleteButton = PushButton(settingsBox, text="Delete", align="left", command=deleteFlavor)
  deleteButton.hide()
  copyFlavorButton = PushButton(settingsBox, text="Copy Selected Flavor", command=copyFlavor, align="left")
  copyFlavorButton.hide()
  flavorsList = ListBox(flavorWindow, items=[flavor.name for flavor in parms.flavors], align="left", height="fill", command=chooseFlavor)
  colorButton = PushButton(flavorWindow, text="Color", width="fill", command=selectColor)
  colorButton.hide()
  currentFlavor = "None"
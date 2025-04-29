import parms
import settings
import homeMenu
import subprocess
import os
from guizero import Window, Box, PushButton, ListBox, TextBox

# Edit Flavor Menu
def editFlavor():
  def saveAndCloseWindow():
    settings.saveSettings()
    homeMenu.updateDrinkNameLists()
    closeWindow()

  def closeWindow():
    flavorWindow.hide()
    flavorWindow.destroy()

  def createNewFlavor():
    if ("New Flavor" in flavorsList.items):
      flavorsList.value = "New Flavor"
    else:
      parms.flavors.append(parms.Flavor("New Flavor", "#ffffff"))
      updateFlavorList()
      flavorsList.value = "New Flavor"

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
      if flavor.name == flavorsList.value:
        del parms.flavors[i]
        chooseFlavor(False)
        break
    for i, chosenFlavor in enumerate(parms.chosenFlavors):
      if chosenFlavor.name == flavorsList.value:
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
  nameText = TextBox(settingsBox, text=currentFlavor, align="top", width="fill")

  # TODO: Uncomment when on Pi
  # nameText.tk.bind("<FocusIn>", show_keyboard)
  # nameText.tk.bind("<FocusOut>", hide_keyboard)
  # nameText.tk.bind("<Return>", on_return)

  def show_keyboard(event=None):
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(["onboard"],env=env)

  def hide_keyboard(event=None):
    subprocess.Popen(["pkill","onboard"])

  def on_return(event=None):
    for i in range(len(parms.flavors)):
      if currentFlavor == parms.flavors[i].name:
        parms.flavors[i].name = nameText.value
    updateFlavorList()
    hide_keyboard()
import parms
import settings
import subprocess
import os
import time
import threading
from guizero import Slider, Combo, Window, PushButton, Box, Text, TextBox

def show_keyboard(event=None):
  env = os.environ.copy()
  env["DISPLAY"] = ":0"
  subprocess.Popen(["onboard"],env=env)

def hide_keyboard(event=None):
  subprocess.Popen(["pkill","onboard"])

def on_return(event=None):
  hide_keyboard()

# Edit Selected Drink Menu
def editDrink():
  drink = parms.currentDrink['value']
  if (parms.newDrinkFlag['value']):
    drink = parms.Drink("Enter Drink Name", 0, 0, 0, 0, 0, parms.chosenFlavors[0], parms.chosenFlavors[1], parms.chosenFlavors[2], parms.chosenFlavors[3], "#ffffff")

  # When Exit Button Pressed, Close New Drink Window
  def closeWindow():
    # TODO: Uncomment when on Pi
    # hide_keyboard()
    makeDrinkWindow.hide()
    makeDrinkWindow.destroy()
  
  def editSliderConstraints(slider):
    """Adjusts slider constraints dynamically while ignoring 'None' sliders and hiding unused ones."""
    active_sliders = [s for l, s in zip(flavor_labels, sliders) if l.value != "None"]
    active_sliders.append(carbSlider)  # Always include Carbonation

    total = sum(s.value for s in active_sliders)  
    remaining = max(100 - total, 0)  

    for s in active_sliders:
      if s != slider:  
        s.end = min(100, s.value + remaining)  

      # Hide sliders with 0 value if total is 100
      if total == 100 and s.value == 0:
        s.width = 0  # Hide slider
      else:
        min_width = 50  
        s.width = max(min_width, int((s.end / 100) * parms.max_slider_width))
  
  def saveDrink():
    import homeMenu
    homeMenu.dispenseButton.text = "Select a Drink"
    newDrink = parms.Drink(nameText.value, flavor1Slider.value, flavor2Slider.value, flavor3Slider.value, flavor4Slider.value, carbSlider.value, 
                     flavor1Label.value, flavor2Label.value, flavor3Label.value, flavor4Label.value, colorButton.bg)
    parms.drinks.append(newDrink)

    if ((newDrink.flavor1Perc > 0) and (not newDrink.flavor1Name in parms.chosenFlavors) and (not newDrink.flavor1Name == "None")):
      parms.invalidDrinkNames.append(newDrink.name)
      homeMenu.invalidDrinkList.append(newDrink.name)
    elif ((newDrink.flavor2Perc > 0) and (not newDrink.flavor2Name in parms.chosenFlavors) and (not newDrink.flavor2Name == "None")):
      parms.invalidDrinkNames.append(newDrink.name)
      homeMenu.invalidDrinkList.append(newDrink.name)
    elif ((newDrink.flavor3Perc > 0) and (not newDrink.flavor3Name in parms.chosenFlavors) and (not newDrink.flavor3Name == "None")):
      parms.invalidDrinkNames.append(newDrink.name)
      homeMenu.invalidDrinkList.append(newDrink.name)
    elif ((newDrink.flavor4Perc > 0) and (not newDrink.flavor4Name in parms.chosenFlavors) and (not newDrink.flavor4Name == "None")):
      parms.invalidDrinkNames.append(newDrink.name)
      homeMenu.invalidDrinkList.append(newDrink.name)
    else:
      parms.drinkNames.append(newDrink.name)
      homeMenu.validDrinkList.append(newDrink.name)

    if (not parms.newDrinkFlag['value']):
      parms.drinks.remove(drink)
      if (parms.validDrinkSelection['value']):
        homeMenu.validDrinkList.remove(drink.name)
        parms.drinkNames.remove(drink.name)
      else:
        homeMenu.invalidDrinkList.remove(drink.name)
        parms.invalidDrinkNames.remove(drink.name)

    for i in range(parms.numFavoriteDrinks):
      if (newDrink.name == homeMenu.favoriteDrinkButtons[i].name):
        homeMenu.favoriteDrinkButtons[i].bg = newDrink.color

    parms.modify_value(parms.newDrinkFlag, False)
    settings.saveSettings()
    closeWindow()

  def updateSliders():
    """Updates sliders when a Combo box changes."""
    for label, slider in zip(flavor_labels, sliders):
        if label.value == "None":
            slider.value = 0  # Set slider to 0 if None is selected
            slider.width = 0  # Hide the slider
        else:
            slider.width = parms.max_slider_width  # Restore width for active sliders
    
    editSliderConstraints(None)  # Recalculate constraints

  def deleteDrink():
    import homeMenu
    parms.drinks.remove(drink)
    if (parms.validDrinkSelection['value']):
      homeMenu.validDrinkList.remove(drink.name)
      parms.drinkNames.remove(drink.name)
    else:
      homeMenu.invalidDrinkList.remove(drink.name)
      parms.invalidDrinkNames.remove(drink.name)
    settings.saveSettings()
    homeMenu.dispenseButton.text = "Select a Drink"
    closeWindow()
  
  def changeColor():
    color = "None"
    color = makeDrinkWindow.select_color(color=drink.color)
    if (color == None):
      color = "#ffffff"
    colorButton.bg = color

  makeDrinkWindow = Window(parms.app, title="Create your drink")
  makeDrinkWindow.show(wait=True)
  makeDrinkWindow.set_full_screen()
  settingsBox = Box(makeDrinkWindow, width="fill", align="top")

  exitButton = PushButton(settingsBox, text="Back", command=closeWindow, align="left")

  colorButton = PushButton(makeDrinkWindow, text="Color", command=changeColor, width="fill", align="tops")

  flavorEditterBox = Box(makeDrinkWindow, layout="grid", align="left")

  displayedFlavors = []
  if (parms.newDrinkFlag['value']):
    displayedFlavors.append(parms.chosenFlavors[0])
    displayedFlavors.append(parms.chosenFlavors[1])
    displayedFlavors.append(parms.chosenFlavors[2])
    displayedFlavors.append(parms.chosenFlavors[3])
  else:
    displayedFlavors.append(drink.flavor1Name)
    displayedFlavors.append(drink.flavor2Name)
    displayedFlavors.append(drink.flavor3Name)
    displayedFlavors.append(drink.flavor4Name)

  flavor1Label = Combo(flavorEditterBox, grid=[0,0], options=parms.flavors, command=updateSliders)
  flavor1Label.value = displayedFlavors[0]
  flavor1Slider = Slider(flavorEditterBox, grid=[1,0], command=editSliderConstraints, align="left", height="20")
  flavor1Slider.value = drink.flavor1Perc
  
  flavor2Label = Combo(flavorEditterBox, options=parms.flavors, grid=[0,1], command=updateSliders)
  flavor2Label.value = displayedFlavors[1]
  flavor2Slider = Slider(flavorEditterBox, grid=[1, 1], command=editSliderConstraints, align="left", height="20")
  flavor2Slider.value = drink.flavor2Perc
  
  flavor3Label = Combo(flavorEditterBox, options=parms.flavors, grid=[0,2], command=updateSliders)
  flavor3Label.value = displayedFlavors[2]
  flavor3Slider = Slider(flavorEditterBox, grid=[1,2], command=editSliderConstraints, align="left", height="20")
  flavor3Slider.value = drink.flavor3Perc
  
  flavor4Label = Combo(flavorEditterBox, options=parms.flavors, grid=[0,3], command=updateSliders)
  flavor4Label.value = displayedFlavors[3]
  flavor4Slider = Slider(flavorEditterBox, grid=[1,3], command=editSliderConstraints, align="left", height="20")
  flavor4Slider.value = drink.flavor4Perc
  
  carbLabel = Text(flavorEditterBox, text="Carbonation", grid=[0,4], enabled=False)
  carbSlider = Slider(flavorEditterBox, grid=[1,4], command=editSliderConstraints, align="left", height="20")
  carbSlider.value = drink.carbPerc

  flavor_labels = [flavor1Label, flavor2Label, flavor3Label, flavor4Label]
  sliders = [flavor1Slider, flavor2Slider, flavor3Slider, flavor4Slider]

  updateSliders()

  blur_zone = Box(makeDrinkWindow, width="fill", height="fill")
  blur_zone.tk.bind("<Button-1>", lambda e: makeDrinkWindow.tk.focus())

  saveButton = PushButton(settingsBox, text="Save", align="right", command=saveDrink)
  deleteButton = PushButton(settingsBox, text="Delete", align="left", command=deleteDrink)
  nameText = TextBox(settingsBox, text=drink.name, align="top", width="fill")

  # TODO: Uncomment when on Pi
  # nameText.tk.bind("<FocusIn>", show_keyboard)
  # nameText.tk.bind("<FocusOut>", hide_keyboard)
  # nameText.tk.bind("<Return>", on_return)

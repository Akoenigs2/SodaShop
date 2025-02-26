from guizero import App, Box, PushButton, Slider, ListBox, Window, Text, TextBox, Combo
import csv
app = App()

# Drink Class
class Drink:
  def __init__(self, name, flavor1Perc, flavor2Perc, flavor3Perc, flavor4Perc, carbPerc, flavor1Name, flavor2Name, flavor3Name, flavor4Name):
    self.name = name
    self.flavor1Perc = flavor1Perc
    self.flavor2Perc = flavor2Perc
    self.flavor3Perc = flavor3Perc
    self.flavor4Perc = flavor4Perc
    self.carbPerc = carbPerc
    self.flavor1Name = flavor1Name
    self.flavor2Name = flavor2Name
    self.flavor3Name = flavor3Name
    self.flavor4Name = flavor4Name
  def __repr__(self):
    return f"Drink({self.name}, {self.flavor1Perc}, {self.flavor2Perc}, {self.flavor3Perc}, {self.flavor4Perc}, {self.carbPerc})"

# Constant Variables
editDrinkText = "Create New Drink"
editFlavorText = "Create New Flavor"
# Will have to modify when on PI:
settingsFileName = "C:\personal\SodaShop\Code\Pi\settings.txt" # Nic Laptop: "C:\git\SodaShop\Code\Pi\settings.txt"

# Writable Global Variables
chosenFlavors = ["temp", "temp", "temp", "temp", "temp"]
drinks = []
flavors = []
currentDrink = {'value':Drink("currentDrink",0,0,0,0,0, "temp", "temp", "temp", "temp")}
newDrinkFlag = {'value':False}
validDrinkSelection = {'value':True}
max_slider_width = 400

# To edit values such as currentDrink
def modify_value(data_dict, newValue):
  data_dict['value'] = newValue

# Load Previous Settings
with open(settingsFileName, "r") as settingsContent:
  chosenFlavors[0] = settingsContent.readline()
  chosenFlavors[0] = chosenFlavors[0][:-1]
  chosenFlavors[1] = settingsContent.readline()
  chosenFlavors[1] = chosenFlavors[1][:-1]
  chosenFlavors[2] = settingsContent.readline()
  chosenFlavors[2] = chosenFlavors[2][:-1]
  chosenFlavors[3] = settingsContent.readline()
  chosenFlavors[3] = chosenFlavors[3][:-1]
  chosenFlavors[4] = "None"
  drinkSelect = False

  reader = csv.reader(settingsContent)
  for row in reader:
    if row:
      if (row[0] == editDrinkText):
        drinkSelect = True
      elif (drinkSelect):
        name = row[0]
        flavor1Perc = int(row[1])
        flavor2Perc = int(row[2])
        flavor3Perc = int(row[3])
        flavor4Perc = int(row[4])
        carbPerc = int(row[5])
        percentages = list(map(int, row[1:5]))
        flavor1String = row[6]
        flavor2String = row[7]
        flavor3String = row[8]
        flavor4String = row[9]
        drinks.append(Drink(name, flavor1Perc, flavor2Perc, flavor3Perc, flavor4Perc, carbPerc, flavor1String, flavor2String, flavor3String, flavor4String))
      else:
        flavors.append(row[0])

# Write Settings Function
def saveSettings():
  with open(settingsFileName, "w", newline='') as file:
    file.write(chosenFlavors[0] + "\n")
    file.write(chosenFlavors[1] + "\n")
    file.write(chosenFlavors[2] + "\n")
    file.write(chosenFlavors[3] + "\n")

    writer = csv.writer(file)
    for flavor in flavors:
      writer.writerow([flavor])
    
    writer.writerow([editDrinkText])

    for drink in drinks:
      writer.writerow([drink.name, drink.flavor1Perc, drink.flavor2Perc, drink.flavor3Perc, drink.flavor4Perc, drink.carbPerc, 
                       drink.flavor1Name, drink.flavor2Name, drink.flavor3Name, drink.flavor4Name])

# Edit Selected Drink Menu
def editDrink():
  drink = currentDrink['value']
  if (newDrinkFlag['value']):
    drink = Drink("Enter Drink Name", 0, 0, 0, 0, 0, chosenFlavors[0], chosenFlavors[1], chosenFlavors[2], chosenFlavors[3])

  # When Exit Button Pressed, Close New Drink Window
  def closeWindow():
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
        s.width = max(min_width, int((s.end / 100) * max_slider_width))
  
  def saveDrink():
    newDrink = Drink(nameText.value, flavor1Slider.value, flavor2Slider.value, flavor3Slider.value, flavor4Slider.value, carbSlider.value, 
                     flavor1Label.value, flavor2Label.value, flavor3Label.value, flavor4Label.value)
    drinks.append(newDrink)

    if ((newDrink.flavor1Perc > 0) and (not newDrink.flavor1Name in chosenFlavors) and (not newDrink.flavor1Name == "None")):
      invalidDrinkNames.append(newDrink.name)
      invalidDrinkList.append(newDrink.name)
    elif ((newDrink.flavor2Perc > 0) and (not newDrink.flavor2Name in chosenFlavors) and (not newDrink.flavor2Name == "None")):
      invalidDrinkNames.append(newDrink.name)
      invalidDrinkList.append(newDrink.name)
    elif ((newDrink.flavor3Perc > 0) and (not newDrink.flavor3Name in chosenFlavors) and (not newDrink.flavor3Name == "None")):
      invalidDrinkNames.append(newDrink.name)
      invalidDrinkList.append(newDrink.name)
    elif ((newDrink.flavor4Perc > 0) and (not newDrink.flavor4Name in chosenFlavors) and (not newDrink.flavor4Name == "None")):
      invalidDrinkNames.append(newDrink.name)
      invalidDrinkList.append(newDrink.name)
    else:
      drinkNames.append(newDrink.name)
      validDrinkList.append(newDrink.name)

    if (not newDrinkFlag['value']):
      drinks.remove(drink)
      if (validDrinkSelection['value']):
        validDrinkList.remove(drink.name)
        drinkNames.remove(drink.name)
      else:
        invalidDrinkList.remove(drink.name)
        invalidDrinkNames.remove(drink.name)

    modify_value(newDrinkFlag, False)
    saveSettings()
    closeWindow()

  def updateSliders():
    """Updates sliders when a Combo box changes."""
    for label, slider in zip(flavor_labels, sliders):
        if label.value == "None":
            slider.value = 0  # Set slider to 0 if None is selected
            slider.width = 0  # Hide the slider
        else:
            slider.width = max_slider_width  # Restore width for active sliders
    
    editSliderConstraints(None)  # Recalculate constraints

  makeDrinkWindow = Window(app, title="Create your drink")
  makeDrinkWindow.show(wait=True)
  settingsBox = Box(makeDrinkWindow, width="fill", align="top")

  exitButton = PushButton(settingsBox, text="Back", command=closeWindow, align="left")

  flavorEditterBox = Box(makeDrinkWindow, layout="grid", align="left")

  displayedFlavors = []
  if (newDrinkFlag['value']):
    displayedFlavors.append(chosenFlavors[0])
    displayedFlavors.append(chosenFlavors[1])
    displayedFlavors.append(chosenFlavors[2])
    displayedFlavors.append(chosenFlavors[3])
  else:
    displayedFlavors.append(drink.flavor1Name)
    displayedFlavors.append(drink.flavor2Name)
    displayedFlavors.append(drink.flavor3Name)
    displayedFlavors.append(drink.flavor4Name)

  flavor1Label = Combo(flavorEditterBox, grid=[0,0], options=flavors, command=updateSliders)
  flavor1Label.value = displayedFlavors[0]
  flavor1Slider = Slider(flavorEditterBox, grid=[1,0], command=editSliderConstraints, align="left", height="20")
  flavor1Slider.value = drink.flavor1Perc
  
  flavor2Label = Combo(flavorEditterBox, options=flavors, grid=[0,1], command=updateSliders)
  flavor2Label.value = displayedFlavors[1]
  flavor2Slider = Slider(flavorEditterBox, grid=[1, 1], command=editSliderConstraints, align="left", height="20")
  flavor2Slider.value = drink.flavor2Perc
  
  flavor3Label = Combo(flavorEditterBox, options=flavors, grid=[0,2], command=updateSliders)
  flavor3Label.value = displayedFlavors[2]
  flavor3Slider = Slider(flavorEditterBox, grid=[1,2], command=editSliderConstraints, align="left", height="20")
  flavor3Slider.value = drink.flavor3Perc
  
  flavor4Label = Combo(flavorEditterBox, options=flavors, grid=[0,3], command=updateSliders)
  flavor4Label.value = displayedFlavors[3]
  flavor4Slider = Slider(flavorEditterBox, grid=[1,3], command=editSliderConstraints, align="left", height="20")
  flavor4Slider.value = drink.flavor4Perc
  
  carbLabel = Text(flavorEditterBox, text="Carbonation", grid=[0,4], enabled=False)
  carbSlider = Slider(flavorEditterBox, grid=[1,4], command=editSliderConstraints, align="left", height="20")
  carbSlider.value = drink.carbPerc

  flavor_labels = [flavor1Label, flavor2Label, flavor3Label, flavor4Label]
  sliders = [flavor1Slider, flavor2Slider, flavor3Slider, flavor4Slider]

  updateSliders()

  saveButton = PushButton(settingsBox, text="Save", align="right", command=saveDrink)
  nameText = TextBox(settingsBox, text=drink.name, align="top", width="fill")

# Select Drink Function
def selectDrink(selection):
  for drink in drinks:
    if (selection == drink.name):
      modify_value(currentDrink, drink)
      break
  # Load Selected Drink
  if (validDrinkSelection['value']):
    dispenseButton.text = "Dispense: " + currentDrink['value'].name + "\n"
  else:
    dispenseButton.text = "Not correct flavors, please load: "
    if (not currentDrink['value'].flavor1Name in chosenFlavors) and (currentDrink['value'].flavor1Perc > 0) and (not currentDrink['value'].flavor1Name == "None"):
      dispenseButton.text += currentDrink['value'].flavor1Name + ", "
    if (not currentDrink['value'].flavor2Name in chosenFlavors) and (currentDrink['value'].flavor2Perc > 0) and (not currentDrink['value'].flavor2Name == "None"):
      dispenseButton.text += currentDrink['value'].flavor2Name + ", "
    if (not currentDrink['value'].flavor3Name in chosenFlavors) and (currentDrink['value'].flavor3Perc > 0) and (not currentDrink['value'].flavor3Name == "None"):
      dispenseButton.text += currentDrink['value'].flavor3Name + ", "
    if (not currentDrink['value'].flavor4Name in chosenFlavors) and (currentDrink['value'].flavor4Perc > 0) and (not currentDrink['value'].flavor4Name == "None"):
      dispenseButton.text += currentDrink['value'].flavor4Name + ", "
    dispenseButton.text = dispenseButton.text[:-2] + "\n"
  
  dispenseButton.text += "Needed Flavors: "
  if (currentDrink['value'].flavor1Perc > 0) and (not currentDrink['value'].flavor1Name == "None"):
    dispenseButton.text += currentDrink['value'].flavor1Name + ", "
  if (currentDrink['value'].flavor2Perc > 0) and (not currentDrink['value'].flavor2Name == "None"):
    dispenseButton.text += currentDrink['value'].flavor2Name + ", "
  if (currentDrink['value'].flavor3Perc > 0) and (not currentDrink['value'].flavor3Name == "None"):
    dispenseButton.text += currentDrink['value'].flavor3Name + ", "
  if (currentDrink['value'].flavor4Perc > 0) and (not currentDrink['value'].flavor4Name == "None"):
    dispenseButton.text += currentDrink['value'].flavor4Name + ", "
  dispenseButton.text = dispenseButton.text[:-2]

def selectInvalidDrink(selection):
  modify_value(validDrinkSelection, False)
  selectDrink(selection)

def selectionValidDrink(selection):
  modify_value(validDrinkSelection, True)
  selectDrink(selection)

def createNewDrink():
    modify_value(newDrinkFlag, True)
    editDrink()

# Edit Flavor Menu
def editFlavor(selection):
  def closeWindow():
    flavorWindow.hide()
    flavorWindow.destroy()
    updateDrinkNameLists()

  def createNewFlavor():
    flavorQuestion = flavorWindow.question("Flavor Edit", "Enter new flavor name")
    if (not flavorQuestion in flavors):
      flavors.append(flavorQuestion)
      chooseFlavorList.append(flavorQuestion)

  def chooseFlavor(flavor):
    if (selection == "1"):
      chosenFlavors[0] = flavor
      flavor1Button.text = flavor
    elif (selection == "2"):
      chosenFlavors[1] = flavor
      flavor2Button.text = flavor
    elif (selection == "3"):
      chosenFlavors[2] = flavor
      flavor3Button.text = flavor
    elif (selection == "4"):
      chosenFlavors[3] = flavor
      flavor4Button.text = flavor

    saveSettings()
    closeWindow()

  flavorWindow = Window(app, title="Swap Flavor")
  flavorWindow.show(wait=True)
  settingsBox = Box(flavorWindow, width="fill", align="top")
  exitButton = PushButton(settingsBox, text="Back", command=closeWindow, align="left")
  newFlavorButton = PushButton(settingsBox, text="Create New Flavor", command=createNewFlavor, align="right")

  chooseFlavorList = ListBox(flavorWindow, items=flavors, align="left", height="fill", command=chooseFlavor)

  saveSettings()

def updateDrinkNameLists():
  drinkNames.clear()
  invalidDrinkNames.clear()
  validDrinkList.clear()
  invalidDrinkList.clear()
  for drink in drinks:
    if ((drink.flavor1Perc > 0) and (not drink.flavor1Name in chosenFlavors) and (not drink.flavor1Name == "None")):
      invalidDrinkNames.append(drink.name)
      invalidDrinkList.append(drink.name)
    elif ((drink.flavor2Perc > 0) and (not drink.flavor2Name in chosenFlavors) and (not drink.flavor2Name == "None")):
      invalidDrinkNames.append(drink.name)
      invalidDrinkList.append(drink.name)
    elif ((drink.flavor3Perc > 0) and (not drink.flavor3Name in chosenFlavors) and (not drink.flavor3Name == "None")):
      invalidDrinkNames.append(drink.name)
      invalidDrinkList.append(drink.name)
    elif ((drink.flavor4Perc > 0) and (not drink.flavor4Name in chosenFlavors) and (not drink.flavor4Name == "None")):
      invalidDrinkNames.append(drink.name)
      invalidDrinkList.append(drink.name)
    else:
      drinkNames.append(drink.name)
      validDrinkList.append(drink.name)

# Main Menu Widgets and Logic
drinkNames = []
invalidDrinkNames = []
drinkListBox = Box(app, height="fill", align="right")
validDrinkList = ListBox(drinkListBox, items=drinkNames, height="fill", align="top", command=selectionValidDrink, scrollbar=True)
invalidDrinkList = ListBox(drinkListBox, items=invalidDrinkNames, height="fill", align="bottom", command=selectInvalidDrink, scrollbar = True)
updateDrinkNameLists()

flavorsSettingsBox = Box(app, width="fill", align="top", border=True)
flavor1Button = PushButton(flavorsSettingsBox, text=chosenFlavors[0], align="left", command=editFlavor, args="1")
flavor2Button = PushButton(flavorsSettingsBox, text=chosenFlavors[1], align="left", command=editFlavor, args="2")
flavor3Button = PushButton(flavorsSettingsBox, text=chosenFlavors[2], align="left", command=editFlavor, args="3")
flavor4Button = PushButton(flavorsSettingsBox, text=chosenFlavors[3], align="left", command=editFlavor, args="4")

editDrinkButton = PushButton(flavorsSettingsBox, text="Edit Selected Drink", align="right", command=editDrink)
createNewDrinkButton = PushButton(flavorsSettingsBox, text=editDrinkText, align="right", command=createNewDrink)
dispenseButton = PushButton(app, text="Select Drink", width="fill", height="fill")

app.display()
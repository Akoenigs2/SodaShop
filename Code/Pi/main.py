from guizero import App, Box, PushButton, Slider, ListBox, Window, Text, TextBox
import csv
app = App()

# Drink Class
class Drink:
  def __init__(self, name, flavor1Perc, flavor2Perc, flavor3Perc, flavor4Perc, carbPerc):
    self.name = name
    self.flavor1Perc = flavor1Perc
    self.flavor2Perc = flavor2Perc
    self.flavor3Perc = flavor3Perc
    self.flavor4Perc = flavor4Perc
    self.carbPerc = carbPerc
  def __repr__(self):
    return f"Drink({self.name}, {self.flavor1Perc}, {self.flavor2Perc}, {self.flavor3Perc}, {self.flavor4Perc}, {self.carbPerc})"

# Constant Variables
editDrinkText = "Create New Drink"
settingsFileName = "C:\git\SodaShop\Code\Pi\settings.txt"

# Writable Global Variables
flavors = ["Edit Flavor 1", "Edit Flavor 2", "Edit Flavor 3", "Edit Flavor 4"]
drinks = []
currentDrink = {'value':0}
newDrinkFlag = {'value':False}
max_slider_width = 400

# To edit values such as currentDrink
def modify_value(data_dict, newValue):
  data_dict['value'] = newValue

# Load Previous Settings
with open(settingsFileName, "r") as settingsContent:
  flavors[0] = settingsContent.readline()
  flavors[1] = settingsContent.readline()
  flavors[2] = settingsContent.readline()
  flavors[3] = settingsContent.readline()

  reader = csv.reader(settingsContent)
  for row in reader:
    if row:
      name = row[0]
      percentages = list(map(int, row[1:]))
      drinks.append(Drink(name,*percentages))

# Write Settings Function
def saveSettings():
  with open(settingsFileName, "w", newline='') as file:
    file.write(flavors[0])
    file.write(flavors[1])
    file.write(flavors[2])
    file.write(flavors[3])

    writer = csv.writer(file)
    for drink in drinks:
      writer.writerow([drink.name, drink.flavor1Perc, drink.flavor2Perc, drink.flavor3Perc, drink.flavor4Perc, drink.carbPerc])

# Edit Selected Drink Menu
def editDrink():
  drink = drinks[int(currentDrink['value'])]

  # When Exit Button Pressed, Close New Drink Window
  def closeWindow():
    makeDrinkWindow.hide()
    makeDrinkWindow.destroy()
  
  def editSliderConstraints(slider):
    total = sum(s.value for s in sliders)  # Get total slider value
    remaining = max(100 - total, 0)  # Ensure remaining is non-negative

    for s in sliders:
      if s != slider:  
        s.end = min(100, s.value + remaining)  # Adjust max limit
        
      # Adjust slider width based on its available range
      if s.value == 0 and total == 100:
        s.width = 0  # Hide slider if its value is 0 and total is maxed
      else:
        min_width = 50  # Minimum width for usability
        s.width = max(min_width, int((s.end / 100) * max_slider_width))
  
  def saveDrink():
    newDrink = Drink(nameText.value, flavor1Slider.value, flavor2Slider.value, flavor3Slider.value, flavor4Slider.value, carbSlider.value)
    drinks.append(newDrink)
    drinkList.append(newDrink.name)
    drinkNames.append(newDrink.name)
    if (not newDrinkFlag['value']):
      drinks.remove(drink)
      drinkList.remove(drink.name)
      drinkNames.remove(drink.name)
    modify_value(newDrinkFlag, False)
    saveSettings()
    closeWindow()

  makeDrinkWindow = Window(app, title="Create your drink")
  makeDrinkWindow.show(wait=True)
  settingsBox = Box(makeDrinkWindow, width="fill", align="top")

  exitButton = PushButton(settingsBox, text="Back", command=closeWindow, align="left")

  flavorEditterBox = Box(makeDrinkWindow, layout="grid", align="left")

  flavor1Label = Text(flavorEditterBox, text=flavors[0], grid=[0,0])
  flavor1Slider = Slider(flavorEditterBox, grid=[1,0], command=editSliderConstraints, align="left", height="20")
  flavor1Slider.value = drink.flavor1Perc
  
  flavor2Label = Text(flavorEditterBox, text=flavors[1], grid=[0,1])
  flavor2Slider = Slider(flavorEditterBox, grid=[1, 1], command=editSliderConstraints, align="left", height="20")
  flavor2Slider.value = drink.flavor2Perc
  
  flavor3Label = Text(flavorEditterBox, text=flavors[2], grid=[0,2])
  flavor3Slider = Slider(flavorEditterBox, grid=[1,2], command=editSliderConstraints, align="left", height="20")
  flavor3Slider.value = drink.flavor3Perc
  
  flavor4Label = Text(flavorEditterBox, text=flavors[3], grid=[0,3])
  flavor4Slider = Slider(flavorEditterBox, grid=[1,3], command=editSliderConstraints, align="left", height="20")
  flavor4Slider.value = drink.flavor4Perc
  
  carbLabel = Text(flavorEditterBox, text="Carbonation", grid=[0,4])
  carbSlider = Slider(flavorEditterBox, grid=[1,4], command=editSliderConstraints, align="left", height="20")
  carbSlider.value = drink.carbPerc

  sliders = [flavor1Slider, flavor2Slider, flavor3Slider, flavor4Slider, carbSlider]

  saveButton = PushButton(settingsBox, text="Save", align="right", command=saveDrink)
  nameText = TextBox(settingsBox, text=drink.name, align="top", width="fill")

# Select Drink Function
def selectDrink(selection):

  modify_value(currentDrink, drinkNames.index(selection))
  # Create New Drink Menu
  if (selection == editDrinkText):
    modify_value(newDrinkFlag, True)
    editDrink()
  # Load Selected Drink
  else:
    print(int(currentDrink['value']))
    dispenseButton.text = drinks[int(currentDrink['value'])].name

# Edit Flavor Menu
def editFlavor(selection):
  flavor = app.question("Flavor Edit", "Enter new flavor name")
  if flavor is not None:
    if (selection == "1"):
      flavors[0] = flavor + "\n"
      flavor1Button.text = flavor
    elif (selection == "2"):
      flavors[1] = flavor + "\n"
      flavor2Button.text = flavor
    elif (selection == "3"):
      flavors[2] = flavor + "\n"
      flavor3Button.text = flavor
    elif (selection == "4"):
      flavors[3] = flavor + "\n"
      flavor4Button.text = flavor
  saveSettings()

# Main Menu Widgets and Logic
drinkNames = []
for drink in drinks:
  drinkNames.append(drink.name)
drinkList = ListBox(app, items=drinkNames, height="fill", align="right", command=selectDrink, scrollbar=True)

flavorsSettingsBox = Box(app, width="fill", align="top", border=True)
flavor1Button = PushButton(flavorsSettingsBox, text=flavors[0], align="left", command=editFlavor, args="1")
flavor2Button = PushButton(flavorsSettingsBox, text=flavors[1], align="left", command=editFlavor, args="2")
flavor3Button = PushButton(flavorsSettingsBox, text=flavors[2], align="left", command=editFlavor, args="3")
flavor4Button = PushButton(flavorsSettingsBox, text=flavors[3], align="left", command=editFlavor, args="4")

editDrinkButton = PushButton(flavorsSettingsBox, text="Edit Selected Drink", align="right", command=editDrink)
dispenseButton = PushButton(app, text=drinks[int(currentDrink['value'])].name, width="fill", height="fill")

app.display()
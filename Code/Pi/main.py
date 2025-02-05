from guizero import App, Box, PushButton, Slider, ListBox, Window, Text
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
currentDrink = 1

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
def editDrink(drink):
  # When Exit Button Pressed, Close New Drink Window
  def closeWindow():
    makeDrinkWindow.hide()
    makeDrinkWindow.destroy()
  
  def update_slider_limits(changed_slider, sliders):
    total = sum(s.value for s in sliders)
    remaining = 100 - (total - changed_slider.value)

    # Ensure the changed slider can never exceed its available range
    changed_slider.end = min(100, remaining + changed_slider.value)

    # Update all other sliders' end values
    for s in sliders:
        if s != changed_slider:
            s.end = min(100, remaining + s.value)

  makeDrinkWindow = Window(app, title="Create your drink")
  makeDrinkWindow.show(wait=True)
  settingsBox = Box(makeDrinkWindow, width="fill", align="top")
  exitButton = PushButton(settingsBox, text="Back", command=closeWindow, align="left")
  flavorEditterBox = Box(makeDrinkWindow, layout="grid", align="left")

  flavor1Label = Text(flavorEditterBox, text=flavors[0], grid=[0,0])
  flavor1Slider = Slider(flavorEditterBox, grid=[1,0])
  flavor1Slider.value = drink.flavor1Perc
  
  flavor2Label = Text(flavorEditterBox, text=flavors[1], grid=[0,1])
  flavor2Slider = Slider(flavorEditterBox, grid=[1, 1])
  flavor2Slider.value = drink.flavor2Perc
  
  flavor3Label = Text(flavorEditterBox, text=flavors[2], grid=[0,2])
  flavor3Slider = Slider(flavorEditterBox, grid=[1,2])
  flavor3Slider.value = drink.flavor3Perc
  
  flavor4Label = Text(flavorEditterBox, text=flavors[3], grid=[0,3])
  flavor4Slider = Slider(flavorEditterBox, grid=[1,3])
  flavor4Slider.value = drink.flavor4Perc
  
  carbLabel = Text(flavorEditterBox, text="Carbonation", grid=[0,4])
  carbSlider = Slider(flavorEditterBox, grid=[1,4])
  carbSlider.value = drink.carbPerc

# Select Drink Function
def selectDrink(selection):

  currentDrink = drinkNames.index(selection)
  # Create New Drink Menu
  if (selection == editDrinkText):
    editDrink(drinks[int(currentDrink)])
  # Load Selected Drink
  else:
    dispenseButton.text = drinks[int(currentDrink)].name

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

editDrinkButton = PushButton(flavorsSettingsBox, text="Edit Selected Drink", align="right", command=editDrink, args=[drinks[int(currentDrink)]])
dispenseButton = PushButton(app, text=drinks[int(currentDrink)].name, width="fill", height="fill")

app.display()
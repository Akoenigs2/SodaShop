from guizero import App

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

def init():
    # Make Global
    global editDrinkText
    global editFlavorText
    global settingsFileName
    global app
    global chosenFlavors
    global drinks
    global flavors
    global currentDrink
    global newDrinkFlag
    global validDrinkSelection
    global max_slider_width
    global drinkNames
    global invalidDrinkNames
    global port
    global baudrate
    global chosenFlavorsColors
    global flavorColors

    # Constant Variables
    editDrinkText = "Create New Drink"
    editFlavorText = "Create New Flavor"
    port='/dev/ttyUSB0'
    baudrate=9600
    # Will have to modify when on PI:
    settingsFileName = "C:\personal\SodaShop\Code\Pi\settings.txt" # Nic Laptop: "C:\git\SodaShop\Code\Pi\settings.txt"
    app = App()

    # Writable Global Variables
    chosenFlavors = ["temp", "temp", "temp", "temp"]
    chosenFlavorsColors = ["None", "None", "None", "None"]
    drinks = []
    flavors = []
    flavorColors = []
    currentDrink = {'value':Drink("currentDrink",0,0,0,0,0, "temp", "temp", "temp", "temp")}
    newDrinkFlag = {'value':False}
    validDrinkSelection = {'value':True}
    max_slider_width = 400
    drinkNames = []
    invalidDrinkNames = []

# To edit values such as currentDrink
def modify_value(data_dict, newValue):
    data_dict['value'] = newValue
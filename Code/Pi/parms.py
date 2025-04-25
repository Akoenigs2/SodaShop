from guizero import App
import serial

# Drink Class
class Drink:
  def __init__(self, name, flavor1Perc, flavor2Perc, flavor3Perc, flavor4Perc, carbPerc, flavor1Name, flavor2Name, flavor3Name, flavor4Name, color):
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
    self.color = color
  def __repr__(self):
    return f"Drink({self.name}, {self.flavor1Perc}, {self.flavor2Perc}, {self.flavor3Perc}, {self.flavor4Perc}, {self.carbPerc})"

class Flavor:
   def __init__(self, name, color):
      self.name = name
      self.color = color

def findFlavorFromName(name):
   for flavor in flavors:
    if flavor.name == name:
       return flavor
    
def findDrinkFromName(name):
   for drink in drinks:
      if drink.name == name:
         return drink

def getListOfDrinkNames():
  list = []
  for drink in drinks:
      list.append(drink.name)
  return list

def getListOfFlavorNames():
  list = []
  for flavor in flavors:
    list.append(flavor.name)
  return list

def getListOfValidDrinksNames():
   list = []
   for validDrink in validDrinks:
      list.append(validDrink.name)
   return list

def getListOfInvalidDrinksNames():
   list = []
   for invalidDrink in invalidDrinks:
      list.append(invalidDrink.name)
   return list

def init():
    # Make Global
    global chosenFlavorsIndicator
    global allFlavorsIndicator
    global favoritDrinksIndicator
    global allDrinksIndicator
    global settingsFileName
    global app
    global chosenFlavors
    global drinks
    global flavors
    global currentDrink
    global newDrinkFlag
    global validDrinkSelection
    global max_slider_width
    global validDrinks
    global invalidDrinks
    global ser
    global favoriteDrinks

    # Constant Variables
    chosenFlavorsIndicator = "Chosen Flavors"
    allFlavorsIndicator = "All Flavors"
    favoritDrinksIndicator = "Favorite Drinks"
    allDrinksIndicator = "All Drinks"
    # Will have to modify when on PI:
    settingsFileName = "G:\seniorDesign\SodaShop\Code\Pi\settings.txt" # Work PC: "G:\seniorDesign\SodaShop\Code\Pi\settings.txt" | # Nic Laptop: "C:\git\SodaShop\Code\Pi\settings.txt"
    app = App() 
    app.set_full_screen()

    # Writable Global Variables
    chosenFlavors = []
    drinks = []
    flavors = []
    currentDrink = {'value':Drink("currentDrink",0,0,0,0,0, "temp", "temp", "temp", "temp", "#ffffff")}
    newDrinkFlag = {'value':False}
    validDrinkSelection = {'value':True}
    max_slider_width = 400
    validDrinks = []
    invalidDrinks = []
    favoriteDrinks = []

# To edit values such as currentDrink
def modify_value(data_dict, newValue):
    data_dict['value'] = newValue

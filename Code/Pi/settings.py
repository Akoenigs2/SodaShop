import parms
import csv

def loadSettings():
    # Load Previous Settings
    with open(parms.settingsFileName, "r") as settingsContent:
        reader = csv.reader(settingsContent)
        loadState = "None"
        for row in reader:
          if row:
            if row[0] == parms.chosenFlavorsIndicator:
              loadState = parms.chosenFlavorsIndicator
            elif row[0] == parms.allFlavorsIndicator:
              loadState = parms.allFlavorsIndicator
            elif row[0] == parms.favoritDrinksIndicator:
              loadState = parms.favoritDrinksIndicator
            elif row[0] == parms.allDrinksIndicator:
              loadState = parms.allDrinksIndicator
            else:
              if loadState == parms.chosenFlavorsIndicator:
                loadedFlavor = parms.Flavor(row[0], row[1])
                parms.chosenFlavors.append(loadedFlavor)
              elif loadState == parms.allFlavorsIndicator:
                loadedFlavor = parms.Flavor(row[0], row[1])
                parms.flavors.append(loadedFlavor)
              elif loadState == parms.favoritDrinksIndicator:
                name = row[0]
                flavor1Perc = int(row[1])
                flavor2Perc = int(row[2])
                flavor3Perc = int(row[3])
                flavor4Perc = int(row[4])
                carbPerc = int(row[5])
                flavor1String = row[6]
                flavor2String = row[7]
                flavor3String = row[8]
                flavor4String = row[9]
                color = row[10]
                loadedDrink = parms.Drink(name, flavor1Perc, flavor2Perc, flavor3Perc, flavor4Perc, carbPerc, flavor1String, flavor2String, flavor3String, flavor4String, color)
                parms.favoriteDrinks.append(loadedDrink)
              elif loadState == parms.allDrinksIndicator:
                name = row[0]
                flavor1Perc = int(row[1])
                flavor2Perc = int(row[2])
                flavor3Perc = int(row[3])
                flavor4Perc = int(row[4])
                carbPerc = int(row[5])
                flavor1String = row[6]
                flavor2String = row[7]
                flavor3String = row[8]
                flavor4String = row[9]
                color = row[10]
                loadedDrink = parms.Drink(name, flavor1Perc, flavor2Perc, flavor3Perc, flavor4Perc, carbPerc, flavor1String, flavor2String, flavor3String, flavor4String, color)
                parms.drinks.append(loadedDrink)

# Write Settings Function
def saveSettings():
  with open(parms.settingsFileName, "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow([parms.chosenFlavorsIndicator])
    for chosenFlavor in parms.chosenFlavors:
      writer.writerow([chosenFlavor.name, chosenFlavor.color])
    
    writer.writerow([parms.allFlavorsIndicator])
    for flavor in parms.flavors:
      writer.writerow([flavor.name, flavor.color])

    writer.writerow([parms.favoritDrinksIndicator])
    for favoriteDrink in parms.favoriteDrinks:
       writer.writerow([favoriteDrink.name, favoriteDrink.flavor1Perc, favoriteDrink.flavor2Perc, favoriteDrink.flavor3Perc, favoriteDrink.flavor4Perc, favoriteDrink.carbPerc, 
                       favoriteDrink.flavor1Name, favoriteDrink.flavor2Name, favoriteDrink.flavor3Name, favoriteDrink.flavor4Name, favoriteDrink.color])

    writer.writerow([parms.allDrinksIndicator])
    for drink in parms.drinks:
      writer.writerow([drink.name, drink.flavor1Perc, drink.flavor2Perc, drink.flavor3Perc, drink.flavor4Perc, drink.carbPerc, 
                       drink.flavor1Name, drink.flavor2Name, drink.flavor3Name, drink.flavor4Name, drink.color])

import parms
import csv

def loadSettings():
    # Load Previous Settings
    with open(parms.settingsFileName, "r") as settingsContent:
        reader = csv.reader(settingsContent)
        i = 0
        drinkSelect = False
        for row in reader:
            if row:
              if (row[0] == parms.editDrinkText):
                drinkSelect = True
                while (i < 4):
                  parms.chosenFlavors[i] = "None"
                  parms.chosenFlavorsColors[i] = "#ffffff"
                  i += 1
              elif (i < 4):
                parms.chosenFlavors[i] = row[0]
                parms.chosenFlavorsColors[i] = row[1]
                i += 1
              elif (drinkSelect):
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
                parms.drinks.append(parms.Drink(name, flavor1Perc, flavor2Perc, flavor3Perc, flavor4Perc, carbPerc, flavor1String, flavor2String, flavor3String, flavor4String))
              else:
                  parms.flavors.append(row[0])
                  parms.flavorColors.append(row[1])

# Write Settings Function
def saveSettings():
  with open(parms.settingsFileName, "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow([parms.chosenFlavors[0], parms.chosenFlavorsColors[0]])
    writer.writerow([parms.chosenFlavors[1], parms.chosenFlavorsColors[1]])
    writer.writerow([parms.chosenFlavors[2], parms.chosenFlavorsColors[2]])
    writer.writerow([parms.chosenFlavors[3], parms.chosenFlavorsColors[3]])

    for flavor, color in zip(parms.flavors, parms.flavorColors):
      writer.writerow([flavor, color])
    
    writer.writerow([parms.editDrinkText])

    for drink in parms.drinks:
      writer.writerow([drink.name, drink.flavor1Perc, drink.flavor2Perc, drink.flavor3Perc, drink.flavor4Perc, drink.carbPerc, 
                       drink.flavor1Name, drink.flavor2Name, drink.flavor3Name, drink.flavor4Name])

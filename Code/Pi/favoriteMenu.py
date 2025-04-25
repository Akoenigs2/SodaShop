import parms
import settings
import homeMenu
from guizero import Window, Box, PushButton, ListBox

def editFavorites():
  def closeWindow():
    favoriteEditWindow.hide()
    favoriteEditWindow.destroy()

  def saveAndCloseWindow():
    import homeMenu
    for i in range(parms.numFavoriteDrinks):
      homeMenu.favoriteDrinkButtons[i].text = favoriteDrinkButtons[i].text
    closeWindow()

  def selectFavoriteDrink(selection):
    parms.modify_value(selectedDrink, int(selection))
    for i in range(parms.numFavoriteDrinks):
      favoriteDrinkButtons[i].bg = "#ffffff"
    favoriteDrinkButtons[selectedDrink['value']].bg = "#e0dcdc"

  def chooseDrink(selection):
    parms.favoriteDrinks[selectedDrink['value']].name = selection
    favoriteDrinkButtons[selectedDrink['value']].text = selection
    saveButton.show()

  favoriteEditWindow = Window(parms.app, title="Edit Favorite Drinks")
  favoriteEditWindow.show(wait=True)
  favoriteEditWindow.set_full_screen()
  settingsBox = Box(favoriteEditWindow, width = "fill", align="top")
  exitButton = PushButton(settingsBox, text="Back", command=closeWindow, align="left")
  saveButton = PushButton(settingsBox, text="Save", command=saveAndCloseWindow, align="right")
  saveButton.hide()

  selectedDrink = {'value':0}
  drinkList = ListBox(favoriteEditWindow, items=parms.drinkNames, align="right", height="fill", command=chooseDrink, scrollbar=True)
  favoriteDrinkButtons = []
  for i in range(parms.numFavoriteDrinks):
    favoriteButton = PushButton(favoriteEditWindow, text=parms.favoriteDrinks[i].name, width="fill", height="fill", command=selectFavoriteDrink, args=str(i))
    favoriteDrinkButtons.append(favoriteButton)
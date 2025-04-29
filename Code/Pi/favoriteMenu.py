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
    for i in range(len(parms.favoriteDrinks)):
      for j in range(len(parms.drinks)):
        if favoriteDrinkButtons[i].text == parms.drinks[j].name:
          parms.favoriteDrinks[i] = parms.drinks[j]

    homeMenu.updateFavoriteButtons()
    closeWindow()

  def selectFavoriteDrink(selection):
    parms.modify_value(selectedDrink, int(selection))
    for i in range(len(parms.favoriteDrinks)):
      favoriteDrinkButtons[i].bg = parms.favoriteDrinks[i].color
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
  drinkList = ListBox(favoriteEditWindow, items=parms.getListOfDrinkNames(), align="right", height="fill", command=chooseDrink, scrollbar=True)
  favoriteDrinkButtons = []
  for i in range(len(parms.favoriteDrinks)):
    favoriteButton = PushButton(favoriteEditWindow, text=parms.favoriteDrinks[i].name, width="fill", height="fill", command=selectFavoriteDrink, args=str(i))
    favoriteButton.bg = parms.favoriteDrinks[i].color
    favoriteDrinkButtons.append(favoriteButton)
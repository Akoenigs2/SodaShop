import parms
import settings
import homeMenu
from guizero import Window, Box, PushButton, ListBox

def editFavorites():
  def saveAndCloseWindow():
    import homeMenu
    homeMenu.updateFavoriteButtons()
    favoriteEditWindow.hide()
    favoriteEditWindow.destroy()

  def selectFavoriteDrink(selection):
    parms.modify_value(selectedDrink, int(selection))
    for i in range(len(parms.favoriteDrinks)):
      favoriteDrinkButtons[i].bg = parms.favoriteDrinks[i].color
    favoriteDrinkButtons[selectedDrink['value']].bg = "#e0dcdc"

  def chooseDrink(selection):
    for drink in parms.drinks:
      if selection == drink.name:
        parms.favoriteDrinks[selectedDrink['value']] = drink
    refreshFavoriteButtons()

  def refreshFavoriteButtons():
    for i in range(len(parms.favoriteDrinks)):
      favoriteDrinkButtons[i].text = parms.favoriteDrinks[i].name
      favoriteDrinkButtons[i].bg = parms.favoriteDrinks[i].color
    favoriteDrinkButtons[selectedDrink['value']].bg = "#e0dcdc"

  favoriteEditWindow = Window(parms.app, title="Edit Favorite Drinks")
  favoriteEditWindow.show(wait=True)
  favoriteEditWindow.set_full_screen()
  settingsBox = Box(favoriteEditWindow, width = "fill", align="top")
  exitButton = PushButton(settingsBox, text="Close and Save", command=saveAndCloseWindow, align="left")

  selectedDrink = {'value':0}
  drinkList = ListBox(favoriteEditWindow, items=parms.getListOfDrinkNames(), align="right", height="fill", command=chooseDrink, scrollbar=True)
  favoriteDrinkButtons = []
  for i in range(len(parms.favoriteDrinks)):
    favoriteButton = PushButton(favoriteEditWindow, text=parms.favoriteDrinks[i].name, width="fill", height="fill", command=selectFavoriteDrink, args=str(i))
    favoriteButton.bg = parms.favoriteDrinks[i].color
    favoriteDrinkButtons.append(favoriteButton)
  favoriteDrinkButtons[0].bg = "#e0dcdc"
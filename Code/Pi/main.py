import parms
import homeMenu
import settings

def main():
  parms.init()
  settings.loadSettings()
  homeMenu.home()
  parms.app.display()

main()
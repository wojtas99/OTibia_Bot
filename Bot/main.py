from PyQt5.QtWidgets import QApplication

import Addresses
from Login import LoginTab
import os


def main():
    # Make directories
    os.makedirs("Targeting", exist_ok=True)
    os.makedirs("Settings", exist_ok=True)
    os.makedirs("Waypoints", exist_ok=True)
    os.makedirs("ItemImages", exist_ok=True)
    os.makedirs("Looting", exist_ok=True)
    os.makedirs("Profile", exist_ok=True)
    f = open("Loot.txt", "a")
    f.close()
    app = QApplication([])
    app.setStyle('Fusion')
    app.setStyleSheet(Addresses.dark_theme)

    login_window = LoginTab()
    login_window.show()

    app.exec()


if __name__ == '__main__':
    main()

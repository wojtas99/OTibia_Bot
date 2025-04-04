from PyQt5.QtWidgets import QApplication
import Addresses
import os

from General.SelectTibiaTab import SelectTibiaTab


def main():
    # Make directories
    os.makedirs("Images", exist_ok=True)
    os.makedirs("Save", exist_ok=True)
    os.makedirs("Save/Targeting", exist_ok=True)
    os.makedirs("Save/Settings", exist_ok=True)
    os.makedirs("Save/Waypoints", exist_ok=True)
    os.makedirs("Save/HealingAttack", exist_ok=True)
    app = QApplication([])
    app.setStyle('Fusion')
    app.setStyleSheet(Addresses.dark_theme)
    login_window = SelectTibiaTab()
    login_window.show()

    app.exec()


if __name__ == '__main__':
    main()
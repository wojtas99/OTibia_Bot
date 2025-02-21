import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QSpinBox,
    QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox,
    QPlainTextEdit
)

class SpellShooterUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spell Shooter")

        # --- Główny widget i layout okna ---
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # --- Etykieta z informacją u góry ---
        label_info = QLabel("More important methods come first (Example: Exori Gran above Exori)")
        main_layout.addWidget(label_info)

        # --- GroupBox, żeby nadać ramkę i tytuł ---
        group_box = QGroupBox("Spell Shooter")
        main_layout.addWidget(group_box)

        group_layout = QVBoxLayout()
        group_box.setLayout(group_layout)

        # --- Pole tekstowe z opisem "RT [5 Sqm] 1 NAZWA POTWORA..."
        #     Używam QPlainTextEdit, żeby można było wstawić więcej tekstu
        #     i mieć podobny wygląd do multiline zrzutu ekranu.
        self.plain_text = QPlainTextEdit()
        self.plain_text.setPlainText("RT [5 Sqm] 1 NAZWA POTWORA: rune 3155, area (0%-100%)")
        # Możesz zablokować edycję, jeśli to ma być tylko 'podgląd':
        # self.plain_text.setReadOnly(True)
        self.plain_text.setMaximumHeight(50)  # Aby nie zajmowało za dużo miejsca
        group_layout.addWidget(self.plain_text)

        # --- Wiersz: "Area Rune (avalanche, great fireball, etc)" + "Requires Target" ---
        row1_layout = QHBoxLayout()
        group_layout.addLayout(row1_layout)

        label_area_rune = QLabel("Area Rune (avalanche, great fireball, etc)")
        row1_layout.addWidget(label_area_rune)

        checkbox_requires_target = QCheckBox("Requires Target")
        row1_layout.addWidget(checkbox_requires_target)
        row1_layout.addStretch()  # wypełnienie przestrzeni z prawej strony

        # --- Wiersz: "Monster Name" + "5 Sqm" ---
        row2_layout = QHBoxLayout()
        group_layout.addLayout(row2_layout)

        label_monster_name = QLabel("Monster Name")
        row2_layout.addWidget(label_monster_name)

        label_5sqm = QLabel("5 Sqm")
        row2_layout.addWidget(label_5sqm)
        row2_layout.addStretch()

        # --- Wiersz: "NAZWA POTWORA" (QLineEdit) + "3155" (QSpinBox) ---
        row3_layout = QHBoxLayout()
        group_layout.addLayout(row3_layout)

        line_monster_name = QLineEdit()
        line_monster_name.setPlaceholderText("NAZWA POTWORA")
        row3_layout.addWidget(line_monster_name)

        spin_rune_id = QSpinBox()
        spin_rune_id.setRange(0, 99999)
        spin_rune_id.setValue(3155)
        row3_layout.addWidget(spin_rune_id)

        # --- Wiersz: "Max% 10, Creatures: 1, HP: 0 - 100" ---
        row4_layout = QHBoxLayout()
        group_layout.addLayout(row4_layout)

        label_maxp = QLabel("Max%:")
        row4_layout.addWidget(label_maxp)

        spin_maxp = QSpinBox()
        spin_maxp.setRange(0, 100)
        spin_maxp.setValue(10)
        row4_layout.addWidget(spin_maxp)

        label_creatures = QLabel("Creatures:")
        row4_layout.addWidget(label_creatures)

        spin_creatures = QSpinBox()
        spin_creatures.setRange(1, 100)
        spin_creatures.setValue(1)
        row4_layout.addWidget(spin_creatures)

        label_hp = QLabel("HP: 0 - 100")
        row4_layout.addWidget(label_hp)

        # --- Przycisk "Prepare" ---
        button_prepare = QPushButton("Prepare")
        group_layout.addWidget(button_prepare)

        # --- Przykładowy arkusz stylów, by uzyskać ciemniejsze tło i ramki ---
        self.setStyleSheet("""
            QMainWindow {
                background-color: #666666; /* tło główne okna */
            }
            QGroupBox {
                background-color: #555555;
                border: 1px solid #888888;
                margin-top: 10px;
            }
            QGroupBox:title {
                color: #ffffff;
                subcontrol-position: top left; /* tytuł w lewym górnym rogu */
                padding: 3px;
            }
            QLabel {
                color: #ffffff;
            }
            QPlainTextEdit, QLineEdit, QSpinBox, QCheckBox {
                background-color: #444444;
                color: #ffffff;
                border: 1px solid #888888;
            }
            QPushButton {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #888888;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)

        # Możesz wywołać show() tutaj lub w main()
        self.show()

def main():
    app = QApplication(sys.argv)
    window = SpellShooterUI()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QToolButton
from PyQt5.QtCore import Qt


class ArrowSelector(QWidget):
    def __init__(self, items, parent=None):
        """
        Inicjalizacja widgetu z listą elementów.

        :param items: lista elementów (np. list[str]), które będą wybierane.
        :param parent: opcjonalny rodzic widgetu.
        """
        super().__init__(parent)
        self.items = items
        self.index = 0

        # Utworzenie layoutu horyzontalnego
        layout = QHBoxLayout(self)

        # Przycisk z lewej strony
        self.leftButton = QToolButton(self)
        self.leftButton.setArrowType(Qt.LeftArrow)
        self.leftButton.clicked.connect(self.on_left_clicked)

        self.label = QLabel(self.items[self.index], self)
        self.label.setAlignment(Qt.AlignCenter)

        # Przycisk z prawej strony
        self.rightButton = QToolButton(self)
        self.rightButton.setArrowType(Qt.RightArrow)
        self.rightButton.clicked.connect(self.on_right_clicked)

        # Dodanie elementów do layoutu
        layout.addWidget(self.leftButton)
        layout.addWidget(self.label)
        layout.addWidget(self.rightButton)

        self.setLayout(layout)

    def on_left_clicked(self):
        """Obsługa kliknięcia w lewą strzałkę."""
        self.index = (self.index - 1) % len(self.items)
        self.label.setText(self.items[self.index])

    def on_right_clicked(self):
        """Obsługa kliknięcia w prawą strzałkę."""
        self.index = (self.index + 1) % len(self.items)
        self.label.setText(self.items[self.index])

    def current_item(self):
        """Zwraca aktualnie wybrany element."""
        return self.items[self.index]

    def set_items(self, items):
        """Pozwala na zmianę listy elementów."""
        self.items = items
        self.index = 0
        self.label.setText(self.items[self.index])



import ctypes as c

import win32gui
import win32process

from Addresses import fin_window_name


def read_memory_address(address_read, offsets, option):
    game_name = fin_window_name("Medivia")
    game = win32gui.FindWindow(None, game_name)
    proc_id = win32process.GetWindowThreadProcessId(game)
    proc_id = proc_id[1]
    process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, proc_id)
    address = c.c_void_p(address_read + offsets)
    if option == 2:
        buffer_size = 8
    elif option == 5:
        buffer_size = 256
    else:
        buffer_size = 4

    buffer = c.create_string_buffer(buffer_size)
    result = c.windll.kernel32.ReadProcessMemory(process_handle, address, buffer, buffer_size, c.byref(c.c_size_t()))
    if not result:
        return
    match option:
        case 1:
            return c.cast(buffer, c.POINTER(c.c_int)).contents.value
        case 2:
            return c.cast(buffer, c.POINTER(c.c_ulonglong)).contents.value
        case 3:
            return c.cast(buffer, c.POINTER(c.c_double)).contents.value
        case 4:
            return c.cast(buffer, c.POINTER(c.c_short)).contents.value
        case 5:
            return buffer.value.decode('utf-8')
        case 7:
            return c.cast(buffer, c.POINTER(c.c_byte)).contents.value
        case _:
            return bytes(buffer)

i = 0
while True:
    wartosci = read_memory_address(0x354B5DC1B80,0xC8, 2)
    wartosci = wartosci + 0x08*i
    i += 1
    wartosci = read_memory_address(wartosci, 0, 2)
    if wartosci == 0:
        break
    x = read_memory_address(wartosci, 0x38, 1)
    if not x:
        break
    if x == 65535 or x < 10:
        break
    print("X = ", x)
    y = read_memory_address(wartosci, 0x3C, 1)
    print("Y = ", y)
    z = read_memory_address(wartosci, 0x40, 4)
    print("Z = ", z)
    name = read_memory_address(wartosci, 0xA8, 5)
    print("Name = ", name)
    print()
    print(i)



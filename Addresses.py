import ctypes as c
import threading
import win32gui
import win32process

from Functions.MemoryFunctions import read_pointer_address, read_memory_address

# Keystrokes codes
lParam = [
    0X00480001, 0x00500001, 0X004D0001,  # 8, 2, 6
    0X004B0001, 0X00490001, 0X00470001,  # 4, 9, 7
    0X00510001, 0X004F0001  # 3, 1
]
rParam = [
    0X26, 0x28, 0X27,  # 8, 2, 6
    0x25, 0x21, 0x24,  # 4, 9, 7
    0x22, 0x23  # 3, 1
]

# Locks
walker_Lock = threading.Lock()


# Static addresses
# Character Addresses
my_x_address = None
my_x_address_offset = None
my_y_address = None
my_y_address_offset = None
my_z_address = None
my_z_address_offset = None
my_name_address = None
my_stats_address = None
my_hp_offset = None
my_hp_max_offset = None
my_mp_offset = None
my_mp_max_offset = None
backpack_address = None
backpack_offset = None

# Target Addresses
attack_address = None
attack_address_offset = None
target_x_offset = None
target_y_offset = None
target_z_offset = None
target_hp_offset = None
target_name_offset = None
monsters_on_screen = None
monsters_on_screen_offset = None

# Game Addresses
game_name = None
game = None
base_address = None
process_handle = None
proc_id = None

#  Variables
tibia_version = None
client_name = None

# Coordinates
screen_x = [0] * 1
screen_y = [0] * 1
screen_width = [0] * 1
screen_height = [0] * 1
coordinates_x = [0] * 11
coordinates_y = [0] * 11

# Other Variables
item_link = ""
item_list = {}
icon_image = "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"
background_image = ""


# Medivia Game
def load_medivia() -> None:
    global my_x_address, my_y_address, my_z_address, my_name_address, attack_address
    global target_name_offset, target_x_offset, target_y_offset, target_hp_offset, target_z_offset
    global my_stats_address, my_hp_offset, my_hp_max_offset, my_mp_offset, my_mp_max_offset
    global process_handle, base_address, game, game_name, monsters_on_screen, monsters_on_screen_offset
    global client_name, background_image, item_list, proc_id, backpack_address, backpack_offset

    item_list = "https://wiki.mediviastats.info/File:"
    background_image = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALkSURBVEhLhVbZchpBDMwvxBzmncLGHAUGkvz/n6UPSaNdqKTjGlqta0azkP3xJ/Fb+JV4PB73+/12u31/f1+v18vlcj6fT6fT8Xj8+vra7/efn58fHx/b/4ENVsvVkn/ESljjX1Pefr6ZG4zAor+hCDYNmNkA5YylSmecNWBiDlm8mQ4DzLFWg9hyOLSvyixXYb2OTUD3hiJFADEQNhosFy/csq1qUQlUpCsr9mbPaHewYFGlRQ9HpFjZazmXtSEAlqv7rFgVQRINfExoRSKaBk0rZfIzV2O4QEV0zDail1AuAT5GkfokYLlaLDiEivEY2x00wIcVbpEo7X1Z55qFpJGUDhJ42aB4jcsYDYx5mxBHdaWPBjUBJxg2geKYA0r0q6q1nxsBNqMBmJDP0lMyXQkoEuWF5b8Is5cNrMwvOYKiiEpoRYI8hJMJOof+Cjki50eOPntF2mpj7rMXt4t82sx1JpfMVSNSGqIZYVDtUJjBh1NfOmZ5bmpGzL4HEd2en1qDZL7NgvUAmvmedbjZJRNQ5dSgW8VQEg4GZMAMRc4AzN6AQVZpNAKwIwI8irqwBE01kBGK0UcUG6z5hlm1qkSK3VWw6FFDjwY+/hj99MvCA8CVDajnAwNTKaMZSYucXDIAh/93rCCsrC5izHiZM+4tZgN54eAvok8nk6qhfgathHiYiptwZE0a6PdWuj64BWyilasf5A67gOKslnXGiMLXCKu33RVxVytVi4CVp6clbzSgLBvJwXVFCuQy9F5OYdYBc/kIi6OB1T6T2Kk8MBdv43qqN+3sRGGA3uenCDW5U8waCG2SNqrTcD/VMqHdms2fIsNBhg/hu/U6i5ER1UsnE8c6H1FApwua+zIkRTKAMPJpNqDY1sAqYLVuwqtBd7o65GqPQG7I3mjwvn7HXnwBdomYTXhfQxSKKzb4ZrOJBkZ/fce7O4B3d7++490dwLs7cDgc/PqOd/fdbocS/8J2+xfQVRnrv+UpjwAAAABJRU5ErkJggg=="

    # Static Addresses
    # Character Addresses
    my_x_address = 0XBEF560
    my_y_address = 0XBEF564
    my_z_address = 0XBEF568
    my_stats_address = 0x00BEE4E0
    my_hp_offset = [0X558]
    my_hp_max_offset = [0X560]
    my_mp_offset = [0x590]
    my_mp_max_offset = [0x598]
    backpack_address = 0x00C76718
    backpack_offset = [0x338, 0X48, 0X8]

    # Target Addresses
    attack_address = 0XBEE4E8
    target_name_offset = 0xA8
    target_x_offset = 0x38
    target_y_offset = 0x3C
    target_z_offset = 0x40
    target_hp_offset = 0xE8

    # Game 'n' Client names
    client_name = "Medivia"
    game_name = fin_window_name(client_name)

    # Loading Addresses
    game = win32gui.FindWindow(None, game_name)
    proc_id = win32process.GetWindowThreadProcessId(game)
    proc_id = proc_id[1]
    process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, proc_id)
    modules = win32process.EnumProcessModules(process_handle)
    base_address = modules[0]


# Altaron
def load_altaron() -> None:
    global my_x_address, my_y_address, my_z_address, my_name_address, attack_address
    global target_name_offset, target_x_offset, target_y_offset, target_hp_offset, target_z_offset
    global my_stats_address, my_hp_offset, my_hp_max_offset, my_mp_offset, my_mp_max_offset
    global process_handle, base_address, game, game_name, monsters_on_screen, monsters_on_screen_offset
    global client_name, background_image, item_list, proc_id, backpack_address, backpack_offset

    item_list = "https://wiki.altaron.pl/images/"
    background_image = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALkSURBVEhLhVbZchpBDMwvxBzmncLGHAUGkvz/n6UPSaNdqKTjGlqta0azkP3xJ/Fb+JV4PB73+/12u31/f1+v18vlcj6fT6fT8Xj8+vra7/efn58fHx/b/4ENVsvVkn/ESljjX1Pefr6ZG4zAor+hCDYNmNkA5YylSmecNWBiDlm8mQ4DzLFWg9hyOLSvyixXYb2OTUD3hiJFADEQNhosFy/csq1qUQlUpCsr9mbPaHewYFGlRQ9HpFjZazmXtSEAlqv7rFgVQRINfExoRSKaBk0rZfIzV2O4QEV0zDail1AuAT5GkfokYLlaLDiEivEY2x00wIcVbpEo7X1Z55qFpJGUDhJ42aB4jcsYDYx5mxBHdaWPBjUBJxg2geKYA0r0q6q1nxsBNqMBmJDP0lMyXQkoEuWF5b8Is5cNrMwvOYKiiEpoRYI8hJMJOof+Cjki50eOPntF2mpj7rMXt4t82sx1JpfMVSNSGqIZYVDtUJjBh1NfOmZ5bmpGzL4HEd2en1qDZL7NgvUAmvmedbjZJRNQ5dSgW8VQEg4GZMAMRc4AzN6AQVZpNAKwIwI8irqwBE01kBGK0UcUG6z5hlm1qkSK3VWw6FFDjwY+/hj99MvCA8CVDajnAwNTKaMZSYucXDIAh/93rCCsrC5izHiZM+4tZgN54eAvok8nk6qhfgathHiYiptwZE0a6PdWuj64BWyilasf5A67gOKslnXGiMLXCKu33RVxVytVi4CVp6clbzSgLBvJwXVFCuQy9F5OYdYBc/kIi6OB1T6T2Kk8MBdv43qqN+3sRGGA3uenCDW5U8waCG2SNqrTcD/VMqHdms2fIsNBhg/hu/U6i5ER1UsnE8c6H1FApwua+zIkRTKAMPJpNqDY1sAqYLVuwqtBd7o65GqPQG7I3mjwvn7HXnwBdomYTXhfQxSKKzb4ZrOJBkZ/fce7O4B3d7++490dwLs7cDgc/PqOd/fdbocS/8J2+xfQVRnrv+UpjwAAAABJRU5ErkJggg=="

    # Static Addresses
    # Character Addresses
    my_x_address = 0XBEF560
    my_y_address = 0XBEF564
    my_z_address = 0XBEF568
    my_stats_address = 0x00BEE4E0
    my_hp_offset = [0X558]
    my_hp_max_offset = [0X560]
    my_mp_offset = [0x590]
    my_mp_max_offset = [0x598]
    backpack_address = 0x00C76718
    backpack_offset = [0x338, 0X48, 0X8]

    # Target Addresses
    attack_address = 0XBEE4E8
    target_name_offset = 0xA8
    target_x_offset = 0x38
    target_y_offset = 0x3C
    target_z_offset = 0x40
    target_hp_offset = 0xE8

    # Game 'n' Client names
    client_name = "Altaron"
    game_name = fin_window_name(client_name)

    # Loading Addresses
    game = win32gui.FindWindow(None, game_name)
    proc_id = win32process.GetWindowThreadProcessId(game)
    proc_id = proc_id[1]
    process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, proc_id)
    modules = win32process.EnumProcessModules(process_handle)
    base_address = modules[0]


def fin_window_name(name) -> str:
    """
    Returns a list of window titles that contain "Medivia"
    but do not contain "EasyBot" (case-insensitive).
    """
    matching_titles = []

    def enum_window_callback(hwnd, _):
        window_text = win32gui.GetWindowText(hwnd)
        if name in window_text and "EasyBot" not in window_text:
            matching_titles.append(window_text)

    win32gui.EnumWindows(enum_window_callback, None)
    return matching_titles[0]


# User Interface
dark_theme = """
    QWidget {
        background-color: #2e2e2e;
        color: #ffffff;
    }

    QMainWindow {
        background-color: #2e2e2e;
    }

    QPushButton {
        background-color: #444444;
        border: 1px solid #5e5e5e;
        color: #ffffff;
        padding: 5px;
        border-radius: 5px;
    }

    QPushButton:hover {
        background-color: #555555;
    }

    QPushButton:pressed {
        background-color: #666666;
    }

    QLineEdit, QTextEdit {
        background-color: #3e3e3e;
        border: 1px solid #5e5e5e;
        color: #ffffff;
    }

    QLabel {
        color: #ffffff;
    }

    QMenuBar {
        background-color: #3e3e3e;
    }

    QMenuBar::item {
        background-color: #3e3e3e;
        color: #ffffff;
    }

    QMenuBar::item:selected {
        background-color: #555555;
    }

    QMenu {
        background-color: #3e3e3e;
        color: #ffffff;
    }

    QMenu::item:selected {
        background-color: #555555;
    }

    QScrollBar:vertical {
        background-color: #2e2e2e;
        width: 12px;
    }

    QScrollBar::handle:vertical {
        background-color: #666666;
        min-height: 20px;
        border-radius: 5px;
    }

    QScrollBar::handle:vertical:hover {
        background-color: #888888;
    }

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        background-color: #2e2e2e;
    }
"""































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

# Dictionary of items to loot
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

    # Background image
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

    my_x_screen_address = 0x00C74820
    my_x_screen_offset = [0xED8, 0X20, 0X68, 0X30, 0XD8, 0X120, 0X60]
    my_y_screen_address = 0x00C74820
    my_y_screen_offset = [0xED8, 0X20, 0X68, 0X30, 0XD8, 0X120, 0X64]

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


# We are Dragons Game
def load_wad() -> None:
    global my_x_address, my_y_address, my_z_address, my_name_address, attack_address
    global target_name_offset, target_x_offset, target_y_offset, target_hp_offset, target_z_offset
    global my_stats_address, my_hp_offset, my_hp_max_offset, my_mp_offset, my_mp_max_offset
    global process_handle, base_address, game, game_name, tibia_version, monsters_on_screen, monsters_on_screen_offset
    global client_name, background_image, item_list, proc_id, backpack_address, backpack_offset
    # Background Image
    background_image = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALkSURBVEhLhVbZchpBDMwvxBzmncLGHAUGkvz/n6UPSaNdqKTjGlqta0azkP3xJ/Fb+JV4PB73+/12u31/f1+v18vlcj6fT6fT8Xj8+vra7/efn58fHx/b/4ENVsvVkn/ESljjX1Pefr6ZG4zAor+hCDYNmNkA5YylSmecNWBiDlm8mQ4DzLFWg9hyOLSvyixXYb2OTUD3hiJFADEQNhosFy/csq1qUQlUpCsr9mbPaHewYFGlRQ9HpFjZazmXtSEAlqv7rFgVQRINfExoRSKaBk0rZfIzV2O4QEV0zDail1AuAT5GkfokYLlaLDiEivEY2x00wIcVbpEo7X1Z55qFpJGUDhJ42aB4jcsYDYx5mxBHdaWPBjUBJxg2geKYA0r0q6q1nxsBNqMBmJDP0lMyXQkoEuWF5b8Is5cNrMwvOYKiiEpoRYI8hJMJOof+Cjki50eOPntF2mpj7rMXt4t82sx1JpfMVSNSGqIZYVDtUJjBh1NfOmZ5bmpGzL4HEd2en1qDZL7NgvUAmvmedbjZJRNQ5dSgW8VQEg4GZMAMRc4AzN6AQVZpNAKwIwI8irqwBE01kBGK0UcUG6z5hlm1qkSK3VWw6FFDjwY+/hj99MvCA8CVDajnAwNTKaMZSYucXDIAh/93rCCsrC5izHiZM+4tZgN54eAvok8nk6qhfgathHiYiptwZE0a6PdWuj64BWyilasf5A67gOKslnXGiMLXCKu33RVxVytVi4CVp6clbzSgLBvJwXVFCuQy9F5OYdYBc/kIi6OB1T6T2Kk8MBdv43qqN+3sRGGA3uenCDW5U8waCG2SNqrTcD/VMqHdms2fIsNBhg/hu/U6i5ER1UsnE8c6H1FApwua+zIkRTKAMPJpNqDY1sAqYLVuwqtBd7o65GqPQG7I3mjwvn7HXnwBdomYTXhfQxSKKzb4ZrOJBkZ/fce7O4B3d7++490dwLs7cDgc/PqOd/fdbocS/8J2+xfQVRnrv+UpjwAAAABJRU5ErkJggg=="

    # Static Addresses
    # Character Addresses
    my_x_address = 0xAD552C
    my_y_address = 0xAD5530
    my_z_address = 0xAD5534
    my_name_address = 0x3F5234
    my_stats_address = 0x00AD5250
    my_hp_offset = [0X518]
    my_hp_max_offset = [0x520]
    my_mp_offset = [0x558]
    my_mp_max_offset = [0x560]
    backpack_address = 0x003F87E4
    backpack_offset = [0xF8, 0X308, 0X638, 0X490, 0X320]

    # Target Addresses
    attack_address = 0xAD5254
    target_name_offset = 0x54
    target_x_offset = 0xC
    target_y_offset = 0x10
    target_z_offset = 0x14
    target_hp_offset = 0x6C
    monsters_on_screen = 0x0F2DEBD0
    monsters_on_screen_offset = [0X0, 0X64, 0X64, 0x48]

    # Tibia Version
    tibia_version = 8.0

    # Game 'n' Client names
    client_name = 'WADclient'
    game_name = fin_window_name(client_name)

    # Loading Addresses
    game = win32gui.FindWindow(None, game_name)
    proc_id = win32process.GetWindowThreadProcessId(game)
    proc_id = proc_id[1]
    process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, proc_id)
    modules = win32process.EnumProcessModules(process_handle)
    base_address = modules[0]


def load_altaron() -> None:
    """
    Memory Addresses in Altaron
    :return: None
    """
    global my_x_address, my_y_address, my_z_address, my_name_address, attack_address
    global target_name_offset, target_x_offset, target_y_offset, target_hp_offset, target_z_offset
    global my_stats_address, my_hp_offset, my_hp_max_offset, my_mp_offset, my_mp_max_offset
    global process_handle, base_address, game, game_name, monsters_on_screen, monsters_on_screen_offset
    global client_name, background_image, item_list, proc_id, backpack_address, backpack_offset

    # Background image
    background_image = "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"

    # Static Addresses
    # Character Addresses
    my_x_address = 0X2F72D30
    my_y_address = 0X2F72D34
    my_z_address = 0x2F72D38
    my_name_address = 0x3F5234
    my_stats_address = 0x02F72BC0
    my_hp_offset = [0X44C]
    my_hp_max_offset = [0x450]
    my_mp_offset = [0x454]
    my_mp_max_offset = [0x458]
    backpack_address = 0x02F72440
    backpack_offset = [0x2F8, 0X0, 0X1C, 0X4]

    # Target Addresses
    attack_address = 0x2F72BC4
    target_name_offset = 0x40
    target_x_offset = 0x34
    target_y_offset = 0x38
    target_z_offset = 0x3C
    target_hp_offset = 0x58
    monsters_on_screen = 0x02F71ED0
    monsters_on_screen_offset = [0X708, 0X200, 0XE00, 0X30]

    client_name = "Altaron"
    game_name = fin_window_name(client_name)

    # Loading Addresses
    game = win32gui.FindWindow(None, game_name)
    proc_id = win32process.GetWindowThreadProcessId(game)
    proc_id = proc_id[1]
    process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, proc_id)
    modules = win32process.EnumProcessModules(process_handle)
    base_address = modules[0]


def load_giveria() -> None:
    """
    Memory Addresses in Altaron
    :return: None
    """
    global my_x_address, my_y_address, my_z_address, my_name_address, attack_address
    global target_name_offset, target_x_offset, target_y_offset, target_hp_offset, target_z_offset
    global my_stats_address, my_hp_offset, my_hp_max_offset, my_mp_offset, my_mp_max_offset
    global process_handle, base_address, game, game_name, sqm_size, monsters_on_screen, monsters_on_screen_offset
    global client_name, background_image, item_list, numberEasyBot, proc_id, backpack_address, backpack_offset
    global my_x_address_offset, my_y_address_offset, my_z_address_offset, attack_address_offset

    # Background image
    background_image = "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"

    # Static Addresses
    # Character Addresses
    my_x_address = 0X00DF6B94
    my_x_address_offset = [0x250, 0x24]
    my_y_address = 0X00DF6B94
    my_y_address_offset = [0x250, 0x28]
    my_z_address = 0x00DF6B94
    my_z_address_offset = [0x250, 0x2C]
    my_name_address = 0x3F5234
    my_stats_address = 0x0069A988
    my_hp_offset = [0X0, 0X8, 0X1B4, 0X40, 0X3C]
    my_hp_max_offset = [0X0, 0X8, 0X1B4, 0X40, 0X40]
    my_mp_offset = [0X0, 0X8, 0X1B4, 0X40, 0X44]
    my_mp_max_offset = [0X0, 0X8, 0X1B4, 0X40, 0X48]
    backpack_address = 0x02F72440
    backpack_offset = [0x2F8, 0X0, 0X1C, 0X4]

    # Target Addresses
    attack_address = 0x00DF6B94
    attack_address_offset = [0x134, 0x28]
    target_name_offset = 0x40
    target_x_offset = 0x34
    target_y_offset = 0x38
    target_z_offset = 0x3C
    target_hp_offset = 0x58
    monsters_on_screen = 0x02F71ED0
    monsters_on_screen_offset = [0X708, 0X200, 0XE00, 0X30]

    client_name = "Giveria"
    game_name = fin_window_name("Tibia")

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































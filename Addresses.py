import ctypes as c
import os
import threading
import win32gui
import win32process

from Functions.MemoryFunctions import enable_debug_privilege_pywin32

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

# Game Variables
game_name = None
game = None
base_address = None
process_handle = None
proc_id = None
client_name = None

# Coordinates
screen_x = [0] * 1
screen_y = [0] * 1
battle_x = [0] * 1
battle_y = [0] * 1
screen_width = [0] * 1
screen_height = [0] * 1
coordinates_x = [0] * 11
coordinates_y = [0] * 11

# Other Variables
item_link = ""
item_list = {}


# Medivia Game
def load_medivia() -> None:
    global my_x_address, my_y_address, my_z_address, \
        my_stats_address, my_hp_offset, my_hp_max_offset, my_mp_offset, my_mp_max_offset, \
        backpack_address, backpack_offset, item_link, \
        attack_address, target_name_offset, target_x_offset, target_y_offset, target_z_offset, target_hp_offset, \
        client_name, base_address, game, proc_id, process_handle, game_name

    item_link = 'https://wiki.mediviastats.info/File:'
    # Static Addresses
    # Character Addresses
    my_x_address = 0XBEE560
    my_y_address = 0XBEE564
    my_z_address = 0XBEE568
    my_stats_address = 0x00BEE4E0
    my_hp_offset = [0X558]
    my_hp_max_offset = [0X560]
    my_mp_offset = [0x590]
    my_mp_max_offset = [0x598]
    backpack_address = 0x00C76718
    backpack_offset = [0x338, 0X48, 0X8]

    # Target Addresses
    attack_address = 0xBED4E8
    target_name_offset = 0xA8
    target_x_offset = 0x38
    target_y_offset = 0x3C
    target_z_offset = 0x40
    target_hp_offset = 0xE8

    # Game 'n' Client names
    client_name = "Medivia"
    os.makedirs("Images/" + client_name, exist_ok=True)
    game_name = fin_window_name(client_name)

    # Loading Addresses
    game = win32gui.FindWindow(None, game_name)
    proc_id = win32process.GetWindowThreadProcessId(game)
    proc_id = proc_id[1]
    process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, proc_id)
    modules = win32process.EnumProcessModules(process_handle)
    base_address = modules[0]


# TibiaScape Game
def load_tibiaScape() -> None:
    global my_x_address, my_y_address, my_z_address, \
        my_stats_address, my_hp_offset, my_hp_max_offset, my_mp_offset, my_mp_max_offset, \
        backpack_address, backpack_offset, item_link, \
        attack_address, target_name_offset, target_x_offset, target_y_offset, target_z_offset, target_hp_offset, \
        client_name, base_address, game, proc_id, process_handle, game_name

    item_link = 'https://www.tibia-wiki.net/wiki/Plik:'
    # Static Addresses
    # Character Addresses
    my_x_address = 0xD22490
    my_y_address = 0XD22494
    my_z_address = 0XD22498
    my_stats_address = 0x00D21D90
    my_hp_offset = [0X6C0]
    my_hp_max_offset = [0X6C8]
    my_mp_offset = [0x6F8]
    my_mp_max_offset = [0x700]
    backpack_address = 0x00D2AE78
    backpack_offset = [0X240, 0X30, 0X20, 0XA8, 0XA8, 0XA8, 0X130]

    # Target Addresses
    attack_address = 0XD21DA0
    target_name_offset = 0x48
    target_x_offset = 0x20
    target_y_offset = 0x24
    target_z_offset = 0x28
    target_hp_offset = 0x68

    # Game 'n' Client names
    client_name = "TibiaScape"
    os.makedirs("Images/" + client_name, exist_ok=True)
    game_name = fin_window_name(client_name)
    # Loading Addresses
    game = win32gui.FindWindow(None, game_name)
    proc_id = win32process.GetWindowThreadProcessId(game)
    proc_id = proc_id[1]
    process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, proc_id)
    modules = win32process.EnumProcessModules(process_handle)
    base_address = modules[0]


def load_miracle() -> None:
    global my_x_address, my_y_address, my_z_address, \
        my_stats_address, my_hp_offset, my_hp_max_offset, my_mp_offset, my_mp_max_offset, \
        backpack_address, backpack_offset, item_link, \
        attack_address, target_name_offset, target_x_offset, target_y_offset, target_z_offset, target_hp_offset, \
        client_name, base_address, game, proc_id, process_handle, game_name

    item_link = 'https://www.tibia-wiki.net/wiki/Plik:'
    # Static Addresses
    # Character Addresses
    my_x_address = 0xA2FF1C
    my_y_address = 0xA2FF20
    my_z_address = 0xA2FF24
    my_stats_address = 0x00A2FB30
    my_hp_offset = [0x4A0]
    my_hp_max_offset = [0x4A8]
    my_mp_offset = [0X4D8]
    my_mp_max_offset = [0X4E0]
    backpack_address = 0x00D2AE78
    backpack_offset = [0X240, 0X30, 0X20, 0XA8, 0XA8, 0XA8, 0X130]

    # Target Addresses
    attack_address = 0xA2FB34
    target_name_offset = 0x30
    target_x_offset = 0xC
    target_y_offset = 0x10
    target_z_offset = 0x14
    target_hp_offset = 0x48

    # Game 'n' Client names
    client_name = "Miracle 7.4"
    os.makedirs("Images/" + client_name, exist_ok=True)
    game_name = fin_window_name(client_name)
    # Loading Addresses
    game = win32gui.FindWindow(None, game_name)
    proc_id = win32process.GetWindowThreadProcessId(game)
    proc_id = proc_id[1]
    process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, proc_id)
    modules = win32process.EnumProcessModules(process_handle)
    base_address = modules[0]


def load_dura() -> None:
    global my_x_address, my_y_address, my_z_address, \
        my_stats_address, my_hp_offset, my_hp_max_offset, my_mp_offset, my_mp_max_offset, \
        backpack_address, backpack_offset, item_link, \
        attack_address, target_name_offset, target_x_offset, target_y_offset, target_z_offset, target_hp_offset, \
        client_name, base_address, game, proc_id, process_handle, game_name

    item_link = 'https://www.tibia-wiki.net/wiki/Plik:'
    # Static Addresses
    # Character Addresses
    my_x_address = 0xBDD3CC
    my_y_address = 0xBDD3D0
    my_z_address = 0xBDD3D4
    my_stats_address = 0x00BDD0F4
    my_hp_offset = [0x4A0]
    my_hp_max_offset = [0x4A8]
    my_mp_offset = [0X4D8]
    my_mp_max_offset = [0X4E0]
    backpack_address = 0x00D2AE78
    backpack_offset = [0X240, 0X30, 0X20, 0XA8, 0XA8, 0XA8, 0X130]

    # Target Addresses
    attack_address = 0xBDD0F8
    target_name_offset = 0x30
    target_x_offset = 0xC
    target_y_offset = 0x10
    target_z_offset = 0x14
    target_hp_offset = 0x48

    # Game 'n' Client names
    client_name = "Dura"
    os.makedirs("Images/" + client_name, exist_ok=True)
    game_name = fin_window_name(client_name)
    # Loading Addresses
    game = win32gui.FindWindow(None, game_name)
    proc_id = win32process.GetWindowThreadProcessId(game)
    proc_id = proc_id[1]
    process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, proc_id)
    modules = win32process.EnumProcessModules(process_handle)
    base_address = modules[0]


def load_treasura() -> None:
    global my_x_address, my_y_address, my_z_address, \
        my_stats_address, my_hp_offset, my_hp_max_offset, my_mp_offset, my_mp_max_offset, \
        backpack_address, backpack_offset, item_link, \
        attack_address, target_name_offset, target_x_offset, target_y_offset, target_z_offset, target_hp_offset, \
        client_name, base_address, game, proc_id, process_handle, game_name

    item_link = 'https://www.tibia-wiki.net/wiki/Plik:'
    # Static Addresses
    # Character Addresses
    my_x_address = 0xB8547C
    my_y_address = 0xB85480
    my_z_address = 0xB85484
    my_stats_address = 0x00B85170
    my_hp_offset = [0x470]
    my_hp_max_offset = [0x478]
    my_mp_offset = [0X4A8]
    my_mp_max_offset = [0X4B0]
    backpack_address = 0x00D2AE78
    backpack_offset = [0X240, 0X30, 0X20, 0XA8, 0XA8, 0XA8, 0X130]

    # Target Addresses
    attack_address = 0xB85174
    target_name_offset = 0x30
    target_x_offset = 0xC
    target_y_offset = 0x10
    target_z_offset = 0x14
    target_hp_offset = 0x48

    # Game 'n' Client names
    client_name = "Treasura"
    os.makedirs("Images/" + client_name, exist_ok=True)
    game_name = fin_window_name(client_name)
    # Loading Addresses
    game = win32gui.FindWindow(None, game_name)
    proc_id = win32process.GetWindowThreadProcessId(game)
    proc_id = proc_id[1]
    process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, proc_id)
    modules = win32process.EnumProcessModules(process_handle)
    base_address = modules[0]

def fin_window_name(name) -> str:
    matching_titles = []

    def enum_window_callback(hwnd, _):
        window_text = win32gui.GetWindowText(hwnd)
        if name in window_text and "k" not in window_text:
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

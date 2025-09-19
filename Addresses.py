import ctypes as c
import os
import threading
import win32gui
import win32process

from Functions.MemoryFunctions import enable_debug_privilege_pywin32

enable_debug_privilege_pywin32()
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

# There is 6 types of values
# 1 Byte - 1 byte
# 2 Short - 2 byte
# 3 Int - 4 bytes
# 4 Long - 8 bytes
# 5 Double - Floating point number
# 6 String - Decoding with UTF-8

# Character Addresses
my_x_address = None
my_x_address_offset = None
my_x_type = 3

my_y_address = None
my_y_address_offset = None
my_y_type = 3

my_z_address = None
my_z_address_offset = None
my_z_type = 2

my_stats_address = None

my_hp_offset = None
my_hp_max_offset = None
my_hp_type = 5

my_mp_offset = None
my_mp_max_offset = None
my_mp_type = 5


# Target Addresses
attack_address = None
attack_address_offset = None
my_attack_type = 4

target_x_offset = None
target_x_type = 3

target_y_offset = None
target_y_type = 3

target_z_offset = None
target_z_type = 2

target_hp_offset = None
target_hp_type = 1

target_name_offset = None
target_name_type = 6


# Game Variables
game_name = None
game = None
base_address = None
process_handle = None
proc_id = None
client_name = None
square_size = 75
application_architecture = 32
collect_threshold = 0.8

# Coordinates
screen_x = [0] * 1
screen_y = [0] * 1
battle_x = [0] * 1
battle_y = [0] * 1
screen_width = [0] * 1
screen_height = [0] * 1
coordinates_x = [0] * 12
coordinates_y = [0] * 12

fishing_x = [0] * 4
fishing_y = [0] * 4

# Other Variables
item_list = {}


# Your OTS Client
def load_tibia() -> None:
    global my_x_address, my_x_address_offset, my_y_address, my_y_address_offset, my_z_address, my_z_address_offset,\
        my_stats_address, my_hp_offset, my_hp_max_offset, my_mp_offset, my_mp_max_offset, \
        attack_address, attack_address_offset, target_name_offset, target_x_offset, target_y_offset, target_z_offset, target_hp_offset, \
        client_name, base_address, game, proc_id, process_handle, game_name, \
        square_size, application_architecture, collect_threshold

    # Game variables
    square_size = 75 # In pixels
    application_architecture = 64 # If game 64 - 64Bit 32 - 32 Bit
    collect_threshold = 0.85

    # Character Addresses
    my_x_address = 0xCE38F0
    my_x_address_offset = []

    my_y_address = 0xCE38Ff
    my_y_address_offset = []

    my_z_address = 0xCE38F8
    my_z_address_offset = []

    my_stats_address = 0x00CE2870

    my_hp_offset = [0X568]
    my_hp_max_offset = [0X570]

    my_mp_offset = [0x5A0]
    my_mp_max_offset = [0x5A8]

    # Target Addresses
    attack_address = 0xCE2878
    attack_address_offset = []

    target_x_offset = 0x38

    target_y_offset = 0x3C

    target_z_offset = 0x40

    target_hp_offset = 0xE8

    target_name_offset = 0xA8


    # Game 'n' Client names
    client_name = "Your client name"
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

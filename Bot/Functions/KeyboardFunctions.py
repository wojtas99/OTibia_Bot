import random
import time
import win32api
import win32gui
import Addresses
from Addresses import rParam, lParam, coordinates_x, coordinates_y
from Functions.MouseFunctions import left_click
import win32con


def walk(wpt_direction, my_x, my_y, my_z, map_x, map_y, map_z) -> None:
    x = map_x - my_x
    y = map_y - my_y
    z = map_z - my_z
    if wpt_direction != 0 and wpt_direction < 9:
        if wpt_direction == 1 and (-3 <= y < 0 or (y == 0 == x)) and abs(z) <= 1:  # Walk North
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[0], lParam[0])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[0], lParam[0])
            return
        if wpt_direction == 2 and 0 < y <= 3 and abs(z) <= 1:  # Walk South
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[1], lParam[1])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[1], lParam[1])
            return
        if wpt_direction == 3 and 0 < x <= 3 and abs(z) <= 1:  # Walk East
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[2], lParam[2])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[2], lParam[2])
            return
        if wpt_direction == 4 and -3 <= x < 0 and abs(z) <= 1:  # Walk West
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[3], lParam[3])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[3], lParam[3])
            return
    else:
        if x == 1 and y == 0 and z == 0:  # Walk East
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[2], lParam[2])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[2], lParam[2])
            return
        if x == -1 and y == 0 and z == 0:  # Walk West
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[3], lParam[3])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[3], lParam[3])
            return
        if x == 0 and y == 1 and z == 0:  # Walk South
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[1], lParam[1])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[1], lParam[1])
            return
        if x == 0 and y == -1 and z == 0:  # Walk North
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[0], lParam[0])
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[0], lParam[0])
            return
        if abs(x) <= 7 and abs(y) <= 5 and z == 0:  # Map click
            left_click(coordinates_x[0] + x * 70, coordinates_y[0] + y * 70)
            time.sleep(random.uniform(0.5, 0.7))
            return


def stay_diagonal(my_x, my_y, monster_x, monster_y) -> None:
    x = monster_x - my_x
    y = monster_y - my_y
    if abs(x) == 1 and abs(y) == 1:
        return
    if x == 1 and y == 0:
        if random.randint(0, 1) == 0:
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[0], lParam[0])  # Up key down
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[0], lParam[0])  # Up key up
            return
        else:
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[1], lParam[1])  # Down key down
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[1], lParam[1])  # Down key up
            return
    if x == -1 and y == 0:
        if random.randint(0, 1) == 0:
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[0], lParam[0])  # Up key down
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[0], lParam[0])  # Up key up
            return
        else:
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[1], lParam[1])  # Down key down
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[1], lParam[1])  # Down key up
            return
    if x == 0 and y == 1:
        if random.randint(0, 1) == 0:
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[2], lParam[2])  # Right key down
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[2], lParam[2])  # Right key up
            return
        else:
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[3], lParam[3])  # Left key down
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[3], lParam[3])  # Left key up
            return
    if x == 0 and y == -1:
        if random.randint(0, 1) == 0:
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[2], lParam[2])  # Right key down
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[2], lParam[2])  # Right key up
            return
        else:
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[3], lParam[3])  # Left key down
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[3], lParam[3])  # Left key up
            return


def chaseDiagonal_monster(my_x, my_y, monster_x, monster_y) -> None:
    pass


def chase_monster(my_x, my_y, monster_x, monster_y) -> None:
    x = monster_x - my_x
    y = monster_y - my_y
    if abs(x) == 1 and abs(y) == 1:
        return
    if x < -1 and abs(y) <= 2:
        win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[3], lParam[3])  # Left key down
        win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[3], lParam[3])  # Left key up
        return
        # Move right if the monster is significantly to the right (x > 1)
    elif x > 1 and abs(y) <= 2:
        win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[2], lParam[2])  # Right key down
        win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[2], lParam[2])  # Right key up
        return
        # Move up if the monster is significantly above (y < -1)
    elif y < -1 and abs(x) <= 2:
        win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[0], lParam[0])  # Up key down
        win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[0], lParam[0])  # Up key up
        return
        # Move down if the monster is significantly below (y > 1)
    elif y > 1 and abs(x) <= 2:
        win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, rParam[1], lParam[1])  # Down key down
        win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, rParam[1], lParam[1])  # Down key up
        return
    if abs(x) <= 7 and abs(y) <= 5:  # Map click
        left_click(coordinates_x[0] + x * 70, coordinates_y[0] + y * 70)
        time.sleep(random.uniform(0.5, 0.7))
        return


def press_key(key) -> None:
    if len(key) == 1:
        vk_code = win32api.VkKeyScan(key)
        if vk_code != -1:
            scan_code = win32api.MapVirtualKey(vk_code & 0xFF, 0)
            keydown_lparam = (scan_code << 16) | 0x0001
            keyup_lparam = keydown_lparam | (0x3 << 30)
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, vk_code & 0xFF, keydown_lparam)
            win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, vk_code & 0xFF, keyup_lparam)


def press_hotkey(hotkey) -> None:
    hotkey_index = (((0x003A0001 >> 16) + hotkey) << 16) + 1
    win32gui.PostMessage(Addresses.game, win32con.WM_KEYDOWN, 0x6F + hotkey, hotkey_index)
    win32gui.PostMessage(Addresses.game, win32con.WM_KEYUP, 0x6F + hotkey, hotkey_index)
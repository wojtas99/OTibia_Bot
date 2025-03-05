import threading
import Addresses
from Addresses import coordinates_x, coordinates_y
import win32api, win32con, win32gui
mouse_lock = threading.Lock()


def mouse_function(x_source, y_source, x_dest = 0, y_dest = 0, option = 0) ->None:
    with mouse_lock:
        if option == 1: #  Right Click
            win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x_source, y_source))
            win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(x_source, y_source))
            win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(x_source, y_source))
        if option == 2: #  Left Click
            win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x_source, y_source))
            win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(x_source, y_source))
            win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(x_source, y_source))


def collect_item(loot_x, loot_y, bp_x, bp_y) -> None:
    win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 1, win32api.MAKELONG(bp_x, bp_y))
    win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(bp_x, bp_y))
    win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(bp_x, bp_y))
    win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(bp_x, bp_y))
    win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(bp_x, bp_y))
    return


def right_click(x, y) -> None:
    win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(x, y))
    win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(x, y))
    return


def left_click(x, y) -> None:
    win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(x, y))
    win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(x, y))
    return


def drag_drop(x, y) -> None:
    win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(x, y))
    win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(coordinates_x[0], coordinates_y[0]))
    win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(coordinates_x[0], coordinates_y[0]))
    return


def use_on_me(x, y) -> None:
    win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(x, y))
    win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(coordinates_x[0], coordinates_y[0]))
    win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(coordinates_x[0], coordinates_y[0]))
    win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(coordinates_x[0], coordinates_y[0]))
    return


def manage_collect(x, y, action) -> None:
    if action > 0:
        collect_item(x + Addresses.screen_x[0], y + Addresses.screen_y[0], Addresses.coordinates_x[action], Addresses.coordinates_y[action])
    elif action == 0:
        drag_drop(x + Addresses.screen_x[0], y + Addresses.screen_y[0])
    elif action == -1:
        mouse_function(x + Addresses.screen_x[0], y + Addresses.screen_y[0], option=1)
    elif action == -2:
        mouse_function(x + Addresses.screen_x[0], y + Addresses.screen_y[0], option=2)
        mouse_function(x + Addresses.screen_x[0], y + Addresses.screen_y[0], option=2)
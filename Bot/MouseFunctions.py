import Addresses
from Addresses import coordinates_x, coordinates_y
import win32api
import win32con
import win32gui


def collect_item(loot_x, loot_y, bp_x, bp_y) -> None:
    """
    Simulates collecting an item by dragging it to a backpack.

    Args:
        loot_x (int): X-coordinate of the loot.
        loot_y (int): Y-coordinate of the loot.
        bp_x (int): X-coordinate of the backpack.
        bp_y (int): Y-coordinate of the backpack.

    Returns:
        None
    """
    win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(loot_x, loot_y))
    win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 1, win32api.MAKELONG(bp_x, bp_y))
    win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(bp_x, bp_y))
    win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(bp_x, bp_y))
    win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(bp_x, bp_y))
    win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(bp_x, bp_y))
    return


def right_click(x, y) -> None:
    """
    Simulates a right mouse click at the given coordinates.

    Args:
        x (int): X-coordinate of the click.
        y (int): Y-coordinate of the click.

    Returns:
        None
    """
    x = int(x)
    y = int(y)
    win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(x, y))
    win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(x, y))
    return


def left_click(x, y) -> None:
    """
    Simulates a left mouse click at the given coordinates.

    Args:
        x (int): X-coordinate of the click.
        y (int): Y-coordinate of the click.

    Returns:
        None
    """
    win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(x, y))
    win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(x, y))
    return


def drag_drop(x, y) -> None:
    """
    Simulates a drag-and-drop action from one set of coordinates to another.

    Args:
        x (int): Starting X-coordinate.
        y (int): Starting Y-coordinate.

    Returns:
        None
    """
    win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(x, y))
    win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(coordinates_x[0], coordinates_y[0]))
    win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(coordinates_x[0], coordinates_y[0]))
    return


def use_on_me(x, y) -> None:
    """
    Simulates a 'use on me' action, selecting an object and using it on the player's character.

    Args:
        x (int): X-coordinate of the object to use.
        y (int): Y-coordinate of the object to use.

    Returns:
        None
    """
    win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONDOWN, 2, win32api.MAKELONG(x, y))
    win32gui.PostMessage(Addresses.game, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(x, y))
    win32gui.PostMessage(Addresses.game, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(coordinates_x[0], coordinates_y[0]))
    win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONDOWN, 1, win32api.MAKELONG(coordinates_x[0], coordinates_y[0]))
    win32gui.PostMessage(Addresses.game, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(coordinates_x[0], coordinates_y[0]))
    return

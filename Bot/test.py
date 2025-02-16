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
    buffer = c.create_string_buffer(256)
    buffer_size = 4
    if option == 2:
        buffer_size = 8
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
        case 7:
            return c.cast(buffer, c.POINTER(c.c_byte)).contents.value
        case _:
            return bytes(buffer)

for i in range(0, 5):
    wartosci = read_memory_address(0x5771BD41A40, 0xC8, 2)


    wartosci = wartosci + 0x08*i

    wartosci = read_memory_address(wartosci, 0, 2)

    if not wartosci:
        break

    x = read_memory_address(wartosci, 0x38, 1)
    print("X = ", x)
    y = read_memory_address(wartosci, 0x3C, 1)
    print("Y = ", y)
    z = read_memory_address(wartosci, 0x40, 1)
    print("Z = ", z)
    i += 1

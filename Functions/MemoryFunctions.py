import win32api
import win32con
import win32security
import Addresses
import ctypes as c


# Reads value from memory
def read_memory_address(address_read, offsets, option):
    address = c.c_void_p(Addresses.base_address + address_read + offsets)
    buffer_size = 8
    buffer = c.create_string_buffer(buffer_size)
    result = c.windll.kernel32.ReadProcessMemory(Addresses.process_handle, address, buffer, buffer_size, c.byref(c.c_size_t()))
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
            try:
                decoded_value = buffer.value.decode('utf-8')
            except UnicodeDecodeError:
                decoded_value = "*"
            return decoded_value
        case 7:
            return c.cast(buffer, c.POINTER(c.c_byte)).contents.value
        case _:
            return bytes(buffer)


def read_pointer_address(address_read, offsets, option):
    address = c.c_void_p(Addresses.base_address + address_read)
    buffer_size = 8
    buffer = c.create_string_buffer(buffer_size)
    for offset in offsets:
        result = c.windll.kernel32.ReadProcessMemory(Addresses.process_handle, address, buffer, buffer_size, c.byref(c.c_size_t()))
        if not result:
            return
        address = c.c_void_p(c.cast(buffer, c.POINTER(c.c_int)).contents.value + offset)
    result = c.windll.kernel32.ReadProcessMemory(Addresses.process_handle, address, buffer, buffer_size, c.byref(c.c_size_t()))
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
            try:
                decoded_value = buffer.value.decode('utf-8')
            except UnicodeDecodeError:
                decoded_value = "*"
            return decoded_value
        case 7:
            return c.cast(buffer, c.POINTER(c.c_byte)).contents.value
        case _:
            return bytes(buffer)


def read_targeting_status():
    if Addresses.attack_address_offset is None:
        if Addresses.client_name == 'Tibiantis':
            return read_memory_address(Addresses.attack_address, 0, 1)
        else:
            return read_memory_address(Addresses.attack_address, 0, 2)
    else:
        return read_pointer_address(Addresses.attack_address, Addresses.attack_address_offset, 1)


def read_my_stats():
    current_hp = read_pointer_address(Addresses.my_stats_address, Addresses.my_hp_offset, 3)
    current_max_hp = read_pointer_address(Addresses.my_stats_address, Addresses.my_hp_max_offset, 3)
    current_mp = read_pointer_address(Addresses.my_stats_address, Addresses.my_mp_offset, 3)
    current_max_mp = read_pointer_address(Addresses.my_stats_address, Addresses.my_mp_max_offset, 3)
    return current_hp, current_max_hp, current_mp, current_max_mp


def read_my_wpt():
    if Addresses.my_x_address_offset is None:
        x = read_memory_address(Addresses.my_x_address, 0, 1)
        y = read_memory_address(Addresses.my_y_address, 0, 1)
        z = read_memory_address(Addresses.my_z_address, 0, 7)
        return x, y, z

    else:
        x = read_pointer_address(Addresses.my_x_address, Addresses.my_x_address_offset, 1)
        y = read_pointer_address(Addresses.my_y_address, Addresses.my_y_address_offset, 1)
        z = read_pointer_address(Addresses.my_z_address, Addresses.my_z_address_offset, 4)
        return x, y, z


def read_target_info():
    if Addresses.client_name == 'Tibiantis':
        attack_address = read_memory_address(Addresses.attack_address, 0, 1)
        attack_address = find_address(Addresses.attack_address+Addresses.base_address, attack_address, 1)- Addresses.base_address
        target_x = read_memory_address(attack_address, Addresses.target_x_offset, 1)
        target_y = read_memory_address(attack_address, Addresses.target_y_offset, 1)
        target_z = read_memory_address(attack_address, Addresses.target_z_offset, 7)
        target_name = read_memory_address(attack_address, Addresses.target_name_offset, 5)
        target_hp = read_memory_address(attack_address, Addresses.target_hp_offset, 7)
        return target_x, target_y, target_z, target_name, target_hp
    else:
        attack_address = read_memory_address(Addresses.attack_address, 0, 2) - Addresses.base_address
        target_x = read_memory_address(attack_address, Addresses.target_x_offset, 1)
        target_y = read_memory_address(attack_address, Addresses.target_y_offset, 1)
        target_z = read_memory_address(attack_address, Addresses.target_z_offset, 7)
        target_name = read_memory_address(attack_address, Addresses.target_name_offset, 5)
        target_hp = read_memory_address(attack_address, Addresses.target_hp_offset, 7)
        return target_x, target_y, target_z, target_name, target_hp
    return None


def enable_debug_privilege_pywin32():
    try:
        # Otwórz token bieżącego procesu z odpowiednimi uprawnieniami
        hToken = win32security.OpenProcessToken(
            win32api.GetCurrentProcess(),
            win32con.TOKEN_ADJUST_PRIVILEGES | win32con.TOKEN_QUERY
        )
        # Pobierz identyfikator przywileju SeDebugPrivilege
        privilege_id = win32security.LookupPrivilegeValue(None, win32security.SE_DEBUG_NAME)
        # Włącz przywilej debugowania
        win32security.AdjustTokenPrivileges(hToken, False, [(privilege_id, win32con.SE_PRIVILEGE_ENABLED)])
        return True
    except Exception as e:
        print("Błąd przy włączaniu przywileju debugowania:", e)
        return False


def find_address(base_module, value_to_find, option, size=0x3000):
    for offset in range(base_module+4, base_module + size, 4):
        value = read_memory_address(offset - Addresses.base_address, 0, option)
        if value_to_find == value:
            return offset
    return None









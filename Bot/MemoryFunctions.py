import Addresses
import ctypes as c


# Reads value from memory
def read_memory_address(address_read, offsets, option):
    try:
        address = address_read + Addresses.base_address + offsets
        address = c.c_void_p(address)
        buffer = c.create_string_buffer(256)
        bytes_read = c.c_size_t()
        result = c.windll.kernel32.ReadProcessMemory(
            Addresses.process_handle, address, buffer, 256, c.byref(bytes_read)
        )
        if not result:
            print(f"ReadProcessMemory failed at address: {hex(address.value)}")
            return None
        match option:
            case 1:  # Returns INT value
                return int(c.c_int.from_buffer(buffer).value)
            case 2:  # Returns LONG value
                return c.c_ulonglong.from_buffer(buffer).value
            case 3:  # Returns DOUBLE value
                return c.c_double.from_buffer(buffer).value
            case 4:  # Returns SHORT value
                return c.c_short.from_buffer(buffer).value
            case 7:  # Returns BYTE value
                return c.c_byte.from_buffer(buffer).value
            case _:  # Returns buffer
                return buffer
    except Exception as e:
        print(f"Exception in read_memory_address: {e}")
        return None


# Reads value from memory pointer
def read_pointer_address(address_read, offsets, option):
    try:
        address = Addresses.base_address + address_read
        address = c.c_void_p(address)
        buffer = c.create_string_buffer(256)
        bytes_read = c.c_size_t()
        result = c.windll.kernel32.ReadProcessMemory(Addresses.process_handle, address, buffer, 256, c.byref(bytes_read))
        if result:
            for offset in offsets:
                if option != 2 and Addresses.client_name != "Medivia":
                    address = c.c_int.from_buffer(buffer).value
                else:
                    address = c.c_ulonglong.from_buffer(buffer).value
                address += offset
                address = c.c_void_p(address)
                result = c.windll.kernel32.ReadProcessMemory(Addresses.process_handle, address, buffer, 256, c.byref(bytes_read))
        else:
            return 0
        if result:
            match option:
                case 1:  # Returns INT value
                    return int(c.c_int.from_buffer(buffer).value)
                case 2:  # Returns LONG value
                    return c.c_ulonglong.from_buffer(buffer).value
                case 3:  # Returns DOUBLE value
                    return c.c_double.from_buffer(buffer).value
                case 4:  # Returns SHORT value
                    return c.c_short.from_buffer(buffer).value
                case _:  # Returns buffer
                    return buffer
        else:
            return 0

    except Exception as e:
        print(f"Exception in read_memory_address: {e}")
        return None

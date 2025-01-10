import Addresses
import ctypes as c


# Reads value from memory
def read_memory_address(address_read, offsets, option):
    try:
        # Calculate the full address
        address = Addresses.base_address + address_read + offsets
        address = c.c_void_p(address)
        buffer = c.create_string_buffer(256)
        bytes_read = c.c_size_t()

        # Read memory
        result = c.windll.kernel32.ReadProcessMemory(
            Addresses.process_handle, address, buffer, c.sizeof(buffer), c.byref(bytes_read)
        )
        if not result:
            print(f"ReadProcessMemory failed at address: {hex(address.value)}")
            return None

        # Return the requested type
        match option:
            case 1:  # Returns INT value
                return c.cast(buffer, c.POINTER(c.c_int)).contents.value
            case 2:  # Returns LONG value
                return c.cast(buffer, c.POINTER(c.c_ulonglong)).contents.value
            case 3:  # Returns DOUBLE value
                return c.cast(buffer, c.POINTER(c.c_double)).contents.value
            case 4:  # Returns SHORT value
                return c.cast(buffer, c.POINTER(c.c_short)).contents.value
            case 7:  # Returns BYTE value
                return c.cast(buffer, c.POINTER(c.c_byte)).contents.value
            case _:  # Returns buffer
                return buffer.raw
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

        # Read the base address
        result = c.windll.kernel32.ReadProcessMemory(
            Addresses.process_handle, address, buffer, c.sizeof(buffer), c.byref(bytes_read)
        )
        if not result:
            print(f"Failed to read initial pointer at address: {hex(address.value)}")
            return None

        # Follow the pointer chain
        for offset in offsets:
            address_value = c.cast(buffer, c.POINTER(c.c_ulonglong)).contents.value if option == 2 else \
                            c.cast(buffer, c.POINTER(c.c_int)).contents.value
            address = c.c_void_p(address_value + offset)
            result = c.windll.kernel32.ReadProcessMemory(
                Addresses.process_handle, address, buffer, c.sizeof(buffer), c.byref(bytes_read)
            )
            if not result:
                print(f"Failed to follow pointer chain at address: {hex(address.value)}")
                return None

        # Return the final value
        match option:
            case 1:  # Returns INT value
                return c.cast(buffer, c.POINTER(c.c_int)).contents.value
            case 2:  # Returns LONG value
                return c.cast(buffer, c.POINTER(c.c_ulonglong)).contents.value
            case 3:  # Returns DOUBLE value
                return c.cast(buffer, c.POINTER(c.c_double)).contents.value
            case 4:  # Returns SHORT value
                return c.cast(buffer, c.POINTER(c.c_short)).contents.value
            case _:  # Returns buffer
                return buffer.raw
    except Exception as e:
        print(f"Exception in read_pointer_address: {e}")
        return None

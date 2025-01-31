import Addresses
import ctypes as c


# Reads value from memory
def read_memory_address(address_read, offsets, option):
    try:
        if not isinstance(offsets, int):
            raise ValueError(f"Offsets should be an integer, got: {type(offsets)}")

        address = Addresses.base_address + address_read + offsets
        address = c.c_void_p(address)
        process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, Addresses.proc_id)
        if not process_handle or process_handle == c.c_void_p(0):
            raise OSError(
                f"Failed to open process with PID: {Addresses.proc_id}, error code: {c.windll.kernel32.GetLastError()}")

        buffer_size = {
            1: c.sizeof(c.c_int),
            2: c.sizeof(c.c_ulonglong),
            3: c.sizeof(c.c_double),
            4: c.sizeof(c.c_short),
            7: c.sizeof(c.c_byte),
        }.get(option, 32)

        local_buffer = (c.c_ubyte * buffer_size)()
        bytes_read = c.c_size_t()

        result = c.windll.kernel32.ReadProcessMemory(
            process_handle, address, local_buffer, buffer_size, c.byref(bytes_read)
        )
        if not result or bytes_read.value != buffer_size:
            error_code = c.windll.kernel32.GetLastError()
            raise RuntimeError(f"ReadProcessMemory failed at address {hex(address.value)}, error code: {error_code}")

        match option:
            case 1:
                return c.cast(local_buffer, c.POINTER(c.c_int)).contents.value
            case 2:
                return c.cast(local_buffer, c.POINTER(c.c_ulonglong)).contents.value
            case 3:
                return c.cast(local_buffer, c.POINTER(c.c_double)).contents.value
            case 4:
                return c.cast(local_buffer, c.POINTER(c.c_short)).contents.value
            case 7:
                return c.cast(local_buffer, c.POINTER(c.c_byte)).contents.value
            case _:
                return bytes(local_buffer)
    except Exception as e:
        print(f"Exception in read_memory_address: {e}")
        return None
    finally:
        if 'process_handle' in locals() and process_handle:
            c.windll.kernel32.CloseHandle(process_handle)


def read_pointer_address(address_read, offsets, option):
    try:
        process_handle = c.windll.kernel32.OpenProcess(0x1F0FFF, False, Addresses.proc_id)
        base_address = Addresses.base_address + address_read
        current_address = c.c_void_p(base_address)

        # Adjust sizes: use c_float if you truly want 4 bytes
        buffer_size = {
            1: c.sizeof(c.c_int),  # INT
            2: c.sizeof(c.c_ulonglong),  # LONG (8 bytes)
            3: c.sizeof(c.c_double),  #
            4: c.sizeof(c.c_short),  # SHORT
        }.get(option, 32)

        local_buffer = (c.c_ubyte * buffer_size)()
        bytes_read = c.c_size_t()

        for offset in offsets:
            result = c.windll.kernel32.ReadProcessMemory(
                process_handle,
                current_address,
                local_buffer,
                c.sizeof(c.c_void_p),
                c.byref(bytes_read)
            )
            if not result or bytes_read.value != c.sizeof(c.c_void_p):
                error_code = c.windll.kernel32.GetLastError()
                raise RuntimeError(
                    f"Failed to read pointer at address {hex(current_address.value)}, "
                    f"error code: {error_code}"
                )

            # Update current_address with pointer + offset.
            # Logic for reading the pointer itself can be adjusted if needed:
            if option == 2:  # LONG value
                pointer_value = c.cast(local_buffer, c.POINTER(c.c_void_p)).contents.value
            elif option != 2 and Addresses.client_name == 'Altaron' or Addresses.client_name == "WADclient":
                pointer_value = c.cast(local_buffer, c.POINTER(c.c_int)).contents.value
            else:
                pointer_value = c.cast(local_buffer, c.POINTER(c.c_void_p)).contents.value

            current_address = c.c_void_p(pointer_value + offset)

        # Final read to get the actual value at the resolved address
        result = c.windll.kernel32.ReadProcessMemory(
            process_handle, current_address, local_buffer, buffer_size, c.byref(bytes_read)
        )
        if not result or bytes_read.value != buffer_size:
            error_code = c.windll.kernel32.GetLastError()
            raise RuntimeError(
                f"Failed to read memory at resolved address {hex(current_address.value)}, "
                f"error code: {error_code}"
            )

        # Return the data based on `option`:
        match option:
            case 1:  # INT
                return c.cast(local_buffer, c.POINTER(c.c_int)).contents.value
            case 2:  # LONG
                return c.cast(local_buffer, c.POINTER(c.c_ulonglong)).contents.value
            case 3:  # FLOAT (was DOUBLE)
                return c.cast(local_buffer, c.POINTER(c.c_double)).contents.value
            case 4:  # SHORT
                return c.cast(local_buffer, c.POINTER(c.c_short)).contents.value
            case _:
                # Fallback: return raw bytes
                return bytes(local_buffer)

    except Exception as e:
        print(f"Exception in read_pointer_address: {e}")
        return None

    finally:
        if 'process_handle' in locals() and process_handle:
            c.windll.kernel32.CloseHandle(process_handle)


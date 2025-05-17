#include <string>
#include <Windows.h>

extern "C" __declspec(dllexport)
DWORD ReadMemory(HANDLE processHandle, DWORD address) {
    DWORD value = 0;
    SIZE_T bytesRead;
    ReadProcessMemory(processHandle, reinterpret_cast<LPCVOID>(address), &value, sizeof(value), &bytesRead);
    return value;
}

extern "C" __declspec(dllexport)
uintptr_t ReadPointer(HANDLE processHandle, uintptr_t address, DWORD* offsets, int num_offsets) {
    ReadProcessMemory(processHandle, reinterpret_cast<LPCVOID>(address), &address, sizeof(address), NULL);
    for (int i = 0; i < num_offsets - 1; ++i) {
        ReadProcessMemory(processHandle, reinterpret_cast<LPCVOID>(address + offsets[i]), &address, sizeof(address), NULL);
    }
    address += offsets[num_offsets - 1];
    return address;
}


extern "C" __declspec(dllexport)
BOOL ReadString(HANDLE processHandle, uintptr_t address, char* buffer, SIZE_T bufferSize) {
    SIZE_T bytesRead = 0;
    BOOL success = ReadProcessMemory(processHandle, (LPCVOID)address, buffer, bufferSize - 1, &bytesRead);
    if (success) buffer[bytesRead] = '\0';
    return success;
}




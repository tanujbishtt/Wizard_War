#include <windows.h>

int WINAPI WinMain(HINSTANCE, HINSTANCE, LPSTR, int) {
    STARTUPINFOW si = { sizeof(si) };
    PROCESS_INFORMATION pi;

    // 1. Start Backend.exe
    CreateProcessW(
        L"Backend\\Backend.exe",   // wide string
        NULL,
        NULL, NULL,
        FALSE,
        CREATE_NO_WINDOW,
        NULL,
        NULL,
        &si,
        &pi
    );

    // 2. Wait 5 seconds
    Sleep(5000);

    // 3. Start Game.exe
    CreateProcessW(
        L"game\\GesturePvP.console.exe",
        NULL,
        NULL, NULL,
        FALSE,
        0,
        NULL,
        NULL,
        &si,
        &pi
    );

    return 0;
}

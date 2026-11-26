#include "ConsoleFunctions.h"
#include <string.h>
using namespace std;
ConsoleFunctions::ConsoleFunctions() : InRec{}, csbi{}
{
    hIn = GetStdHandle(STD_INPUT_HANDLE);
    hOut = GetStdHandle(STD_OUTPUT_HANDLE);
}

void ConsoleFunctions::setConsoleTitle(const char *title)
{
    SetConsoleTitleA(title);
}

void ConsoleFunctions::SetCursorAt(int x, int y)
{
    COORD coord;
    coord.X = x;
    coord.Y = y;
    SetConsoleCursorPosition(hOut, coord);
}

char ConsoleFunctions::ReadFrom(int x, int y)
{
    DWORD nLength = 1;                             // The number of chars to read, we need to read one character only!
    char *str = new char[nLength * sizeof(TCHAR)]; // Buffer of 1 char size
    COORD readFromCoord;                           // Co-ordinates from where to read
    readFromCoord.X = x;
    readFromCoord.Y = y;
    DWORD num_read = 0; // Will be set to no. of charaters actually read
    ReadConsoleOutputCharacter(hOut, (LPTSTR)str, nLength, readFromCoord, (LPDWORD)&num_read);
    return *str;
}

void ConsoleFunctions::DetectEvent()
{
    DWORD nLength = 1;  // The number of records to read, we need to read one record only!
    DWORD num_read = 0; // Will be set to no. of input records actually read

    ReadConsoleInput(hIn, &InRec, nLength, &num_read);
}

void ConsoleFunctions::getMousePosition(point &p)
{
    p.x = InRec.Event.MouseEvent.dwMousePosition.X;
    p.y = InRec.Event.MouseEvent.dwMousePosition.Y;
}

bool ConsoleFunctions::IsMouseLeftClickEvent(point &p)
{
    if (InRec.EventType == MOUSE_EVENT && InRec.Event.MouseEvent.dwButtonState == FROM_LEFT_1ST_BUTTON_PRESSED)
    {
        p.x = InRec.Event.MouseEvent.dwMousePosition.X;
        p.y = InRec.Event.MouseEvent.dwMousePosition.Y;
        return true;
    }

    return false;
}

bool ConsoleFunctions::IsMouseRightClickEvent(point &p)
{
    if (InRec.EventType == MOUSE_EVENT && InRec.Event.MouseEvent.dwButtonState == RIGHTMOST_BUTTON_PRESSED)
    {
        p.x = InRec.Event.MouseEvent.dwMousePosition.X;
        p.y = InRec.Event.MouseEvent.dwMousePosition.Y;
        return true;
    }
    return false;
}

bool ConsoleFunctions::IsKeyPressEvent(char &key)
{
    if (InRec.EventType == KEY_EVENT && InRec.Event.KeyEvent.bKeyDown)
    {
        /*WORD virtualKey = InRec.Event.KeyEvent.wVirtualKeyCode;
        if (virtualKey == VK_LEFT) {
            std::cout << "Pressed: LEFT ARROW\n";
        }*/
        // To DETECT Arrow key left
        key = InRec.Event.KeyEvent.uChar.AsciiChar;
        return true;
    }
    return false;
}

bool ConsoleFunctions::IsKeyReleaseEvent(char &key)
{
    if (InRec.EventType == KEY_EVENT && !InRec.Event.KeyEvent.bKeyDown)
    {
        key = InRec.Event.KeyEvent.uChar.AsciiChar;
        return true;
    }
    return false;
}

int ConsoleFunctions::getTextColor()
{
    GetConsoleScreenBufferInfo(hOut, &csbi);
    int a = csbi.wAttributes;
    return a % 16;
}

int ConsoleFunctions::getBackColor()
{
    GetConsoleScreenBufferInfo(hOut, &csbi);
    int a = csbi.wAttributes;
    return (a / 16) % 16;
}

void ConsoleFunctions::SetColor(ConsoleColor textcol, ConsoleColor backcol)
{
    SetColor(int(textcol), int(backcol));
}

void ConsoleFunctions::SetColor(int textcol, int backcol)
{
    bool textcolorprotect = true; // for future use
    /*doesn't let textcolor be the same as backgroung color if true*/
    if (textcolorprotect)
    {
        if ((textcol % 16) == (backcol % 16))
            textcol++;
    }
    textcol %= 16;
    backcol %= 16;
    unsigned short wAttributes = (unsigned)textcol | ((unsigned)backcol << 4);
    SetConsoleTextAttribute(hOut, wAttributes);
}

void ConsoleFunctions::clearConsole()
{
    COORD home = { 0, 0 };
    DWORD written;
    if (!GetConsoleScreenBufferInfo(hOut, &csbi)) return;
    DWORD size = csbi.dwSize.X * csbi.dwSize.Y;
    FillConsoleOutputCharacter(hOut, ' ', size, home, &written);
    FillConsoleOutputAttribute(hOut, csbi.wAttributes, size, home, &written);
    SetConsoleCursorPosition(hOut, home);
}
ConsoleFunctions::~ConsoleFunctions()
{
}
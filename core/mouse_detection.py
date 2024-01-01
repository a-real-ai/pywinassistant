import ctypes
import win32api
import win32con

# Define the CURSORINFO structure
class CURSORINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_int),
                ("flags", ctypes.c_int),
                ("hCursor", ctypes.c_void_p),
                ("ptScreenPos", ctypes.c_long * 2)]

def get_cursor_shape():
    cursor_info = CURSORINFO()
    cursor_info.cbSize = ctypes.sizeof(CURSORINFO)
    ctypes.windll.user32.GetCursorInfo(ctypes.byref(cursor_info))

    # Load the standard cursors to compare
    cursor_arrow = win32api.LoadCursor(0, win32con.IDC_ARROW)
    cursor_ibeam = win32api.LoadCursor(0, win32con.IDC_IBEAM)
    cursor_hand = win32api.LoadCursor(0, win32con.IDC_HAND)
    cursor_wait = win32api.LoadCursor(0, win32con.IDC_WAIT)
    cursor_cross = win32api.LoadCursor(0, win32con.IDC_CROSS)

    # Compare the current cursor with the standard cursors
    if cursor_info.hCursor == cursor_arrow:
        return "Arrow"
    elif cursor_info.hCursor == cursor_ibeam:
        return "The cursor is active for Text Input (I-beam)"
    elif cursor_info.hCursor == cursor_hand:
        return "The cursor is 'Hand' (A link is select)"
    elif cursor_info.hCursor == cursor_wait:
        return "The cursor is 'Wait' (Busy) - Hourglass or Watch"
    elif cursor_info.hCursor == cursor_cross:
        return "The cursor is 'Cross'"
    else:
        return "Other"

# while True:
#     cursor_shape = get_cursor_shape()
#     print(f"Cursor shape: {cursor_shape}")
#     time.sleep(1)

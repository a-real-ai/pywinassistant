import win32com.client
import win32gui
import win32con
import win32process
from datetime import datetime

def enumerate_windows():
    windows = []

    def enum_window_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            windows.append(hwnd)

    win32gui.EnumWindows(enum_window_callback, None)
    return windows

def should_exclude_process(name):
    excluded_processes = ['dwm.exe', 'nvcontainer.exe', 'nvidia broadcast ui.exe', 'system', 'python.exe', 'steam.exe',
                          'TextInputHost.exe', 'tk', 'pycharm64.exe', 'nvidia broadcast.exe', 'widgets.exe',
                          'CTkToplevel', 'Windows Input Experience', 'widgets.exe', 'translucenttb.exe', 
                          'securityhealthsystray.exe', 'Ctk', 'Ctk.exe', 'tk', 'tk.exe', 'Code', 'Code.exe', 'NVIDIA Share.exe',
                          'NVIDIA Web Helper.exe', 'nvsphelper64.exe', 'NVIDIA GeForce Experience.exe',
                          'nvcontainer.exe', 'NVDisplay.Container.exe']
    return name.lower() in excluded_processes

def get_process_name(hwnd):
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    wmi = win32com.client.GetObject('winmgmts:')
    process = wmi.ExecQuery(f'SELECT Name FROM Win32_Process WHERE ProcessId = {pid}')
    if process:
        return process[0].Name
    return None

def get_topmost_window():
    for hwnd in enumerate_windows():
        process_name = get_process_name(hwnd)
        title = win32gui.GetWindowText(hwnd)
        # print(f"Debug: Window Title: '{title}', Process: '{process_name}'")  # Debugging line
        if process_name and not should_exclude_process(process_name):
            return title, process_name
    return None, None

def get_window_handle(title):
    handles = []

    def enum_window_callback(hwnd, _):
        if win32gui.GetWindowText(hwnd) == title:
            handles.append(hwnd)

    win32gui.EnumWindows(enum_window_callback, None)
    return handles[0] if handles else None

def set_foreground_window_by_title(title):
    hwnd = get_window_handle(title)
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        try:
            win32gui.SetForegroundWindow(hwnd)
        except Exception as e:
            print(f"Error setting foreground window: {e}")
    else:
        print(f"Window with title '{title}' not found.")

def focus_topmost_window():
    topmost_window_title, _ = get_topmost_window()  # We're not using process_name here
    if topmost_window_title:
        print(f"Selected application: {topmost_window_title}")
        set_foreground_window_by_title(topmost_window_title)
        return topmost_window_title
    else:
        print("No suitable windows found.")

# Example usage
# focus_topmost_window()

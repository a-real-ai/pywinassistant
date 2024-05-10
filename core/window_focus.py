import subprocess
import os
import ctypes
import sys
import time
import winreg
from fuzzywuzzy import fuzz
import pygetwindow as gw
import uiautomation as auto
import win32gui
import win32process
import psutil
import winreg

# Define necessary functions from the user32 DLL
user32 = ctypes.WinDLL('user32', use_last_error=True)
EnumWindows = user32.EnumWindows
GetForegroundWindow = user32.GetForegroundWindow
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
GetWindowThreadProcessId = user32.GetWindowThreadProcessId
GetWindowTextLength = user32.GetWindowTextLengthW
GetWindowText = user32.GetWindowTextW
IsWindowVisible = user32.IsWindowVisible
SetForegroundWindow = user32.SetForegroundWindow
IsIconic = user32.IsIconic
ShowWindow = user32.ShowWindow

# Constants for ShowWindow function
SW_RESTORE = 9
SW_SHOW = 5

def get_installed_apps_registry():
    installed_apps = []
    reg_paths = [
        r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
        r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
    ]
    for reg_path in reg_paths:
        with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
            with winreg.OpenKey(hkey, reg_path, 0, winreg.KEY_READ) as sub_key:
                subkey_count, _, _ = winreg.QueryInfoKey(sub_key)
                for i in range(subkey_count):
                    try:
                        subkey_name = winreg.EnumKey(sub_key, i)
                        with winreg.OpenKey(sub_key, subkey_name) as app_key:
                            app_name, _ = winreg.QueryValueEx(app_key, 'DisplayName')
                            installed_apps.append(app_name)
                    except EnvironmentError:
                        continue
    return installed_apps


def get_open_windows():
    excluded_titles = ["AI Drone Assistant", "NVIDIA GeForce Overlay", "Windows Input Experience", "Program Manager"]
    excluded_executables = ["NVIDIA Share.exe", "TextInputHost.exe", "Tk.exe", "conhost.exe", "explorer.exe",
                            "CTkToplevel", 'Windows Input Experience', "SecurityHealthSystray.exe", "Steam.exe",
                            "SearchApp.exe", "ApplicationFrameHost.exe", "ShellExperienceHost.exe", "MicrosoftEdge.exe",
                            "MicrosoftEdgeCP.exe", "MicrosoftEdgeSH.exe", "python.exe", "pycharm64.exe", "pycharm64.exe",
                            "Ctk", "Ctk.exe", "tk", "tk.exe", "Code", "Code.exe", "amdow.exe",
                            "nvidia broadcast.exe", "nvidia broadcast ui.exe", "NVIDIA Share.exe",
                            "NVIDIA Web Helper.exe", "nvsphelper64.exe", "NVIDIA GeForce Experience.exe",
                            "nvcontainer.exe", "NVDisplay.Container.exe"]

    windows = gw.getAllWindows()
    print(windows)
    open_windows_info = []
    for w in windows:
        if (w.visible and not w.isMinimized and w.title and w.height > 100 and w.width > 100
                and w.title not in excluded_titles):
            hwnd = w._hWnd
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            executable_name = process.name()
            if executable_name not in excluded_executables:
                rect = win32gui.GetWindowRect(hwnd)
                position = (rect[0], rect[1])
                size = (rect[2] - rect[0], rect[3] - rect[1])
                open_windows_info.append((w.title, position, size, executable_name, w))
    # Sort the windows by their Z position (from top to bottom)
    open_windows_info.sort(key=lambda x: x[1][1], reverse=True)
    return [info[:-1] for info in open_windows_info]  # Exclude the window object from the returned info


def get_window_text(hwnd):
    length = GetWindowTextLength(hwnd) + 1
    buffer = ctypes.create_unicode_buffer(length)
    GetWindowText(hwnd, buffer, length)
    return buffer.value


def get_active_window_title():
    time.sleep(1) # Wait for the window to be fully active ToDo: Fix this part!
    hwnd = GetForegroundWindow()
    return get_window_text(hwnd)


def enum_windows_proc(hwnd, lParam):
    if IsWindowVisible(hwnd):
        title = get_window_text(hwnd)
        if title:
            hwnd_list.append((hwnd, title))
    return True


def open_windows_info():
    global hwnd_list
    hwnd_list = []
    EnumWindows(EnumWindowsProc(enum_windows_proc), 0)
    return hwnd_list


def find_window(partial_title):
    windows = open_windows_info()
    for hwnd, title in windows:
        if partial_title.lower() in title.lower():
            return hwnd
    return None


def find_window_by_title(partial_title):
    windows = open_windows_info()
    for hwnd, title in windows:
        if partial_title.lower() in title.lower():
            return hwnd, title
    return None, None


def bring_to_foreground(hwnd):
    if IsIconic(hwnd):
        ShowWindow(hwnd, SW_RESTORE)
    else:
        ShowWindow(hwnd, SW_SHOW)
    SetForegroundWindow(hwnd)


def search_registry_for_application(app_name):
    sub_keys = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
    ]
    registry_hives = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]

    for hive in registry_hives:
        for sub_key in sub_keys:
            try:
                with winreg.OpenKey(hive, sub_key) as key:
                    for i in range(0, winreg.QueryInfoKey(key)[0]):
                        skey_name = winreg.EnumKey(key, i)
                        skey = winreg.OpenKey(key, skey_name)
                        try:
                            display_name = winreg.QueryValueEx(skey, 'DisplayName')[0]
                            if app_name.lower() in display_name.lower():
                                # Look for the executable in a 'DisplayIcon' field
                                try:
                                    executable_path = winreg.QueryValueEx(skey, 'DisplayIcon')[0]
                                    # In case the path points to an icon, it usually contains a comma
                                    # followed by an icon index, e.g. "C:\Path\To\App.exe,0"
                                    if ',' in executable_path:
                                        executable_path = executable_path.split(',')[0]
                                    return executable_path
                                except OSError:
                                    pass

                                # If not found, fall back to 'UninstallString' as a last resort
                                uninstall_string = winreg.QueryValueEx(skey, 'UninstallString')[0]
                                # Here you would need to intelligently extract the executable path
                                # This might involve more complex logic and is not guaranteed to work
                                # for all applications as uninstall strings can vary significantly.
                                # This is a starting point that might work for some applications:
                                # uninstall_string = uninstall_string.split('"')[1] if '"' in uninstall_string else uninstall_string
                                # return uninstall_string if os.path.isfile(uninstall_string) else None
                        except OSError:
                            pass
                        finally:
                            skey.Close()
            except OSError:
                pass
    return None

def find_best_match_window(partial_title, threshold=50):
    windows = open_windows_info()
    best_match = None
    highest_score = 0
    for hwnd, title in windows:
        score = fuzz.token_sort_ratio(partial_title.lower(), title.lower())
        if score > highest_score and score >= threshold:
            best_match = (hwnd, title)
            highest_score = score
    return best_match


# def activate_windowt_title(application_name):
#     print(f"Activating window for {application_name}")
#     if application_name.lower() == "cmd":
#         # If we know it's cmd, we can try activating an existing window or start a new one directly
#         hwnd, window_title = find_window_by_title("cmd")
#         if hwnd:
#             # If we found a window, bring it to the foreground
#             bring_to_foreground(hwnd)
#         else:
#             os.startfile('cmd.exe')
#         return get_active_window_title()
#     app_path = None
#
#     # Attempt to find the application path for each word in application_name
#
#     process = subprocess.run(['where', application_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
#                              shell=True)
#     output = process.stdout.strip().split('\n')
#     app_path = output[0] if output else None
#     print(f"Application path: {app_path}")
#     # If the application path wasn't found, search in the registry for each word
#     if not app_path:
#         print(f"Searching in registry for application path for '{application_name}'...")
#         app_path = search_registry_for_application(application_name)
#
#     hwnd, window_title = None, None
#     hwnd, window_title = find_window_by_title(application_name)
#     if window_title:
#         bring_to_foreground(hwnd)
#     elif app_path:
#         print("Application found but no window open. Starting the application...")
#         print(f"Application path: {app_path}")
#         subprocess.Popen(app_path)  # Open the application if it is not running
#     else:
#         print(f"{application_name} could not be found nor is open. Please ensure it is installed and accessible via system PATH.")
#     return get_active_window_title()

def activate_windowt_title(application_name):
    if application_name.lower() == "cmd":
        # If we know it's cmd, we can try activating an existing window or start a new one directly
        hwnd, window_title = find_window_by_title("cmd")
        if hwnd:
            # If we found a window, bring it to the foreground
            bring_to_foreground(hwnd)
        else:
            os.startfile('cmd.exe')
        return get_active_window_title()

    app_path = None
    words = application_name.split()

    # Attempt to find the application path for each word in application_name
    for word in words:
        try:
            process = subprocess.run(['where', word], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                     shell=True)
            output = process.stdout.strip().split('\n')
            if output:
                app_path = output[0]
                break  # Once we have found a path, we can break the loop
        except Exception as e:
            print(f"ERROR: Error finding application path for '{word}': {e}")

    # If the application path wasn't found, search in the registry for each word
    if not app_path:
        for word in words:
            app_path = search_registry_for_application(word)
            if app_path:
                break  # Once we have found a path, we can break the loop

    hwnd, window_title = None, None
    # Attempt to find the window with a partial match for any of the words
    for word in words:
        hwnd, window_title = find_window_by_title(word)
        if hwnd:
            break  # Once we have found a window, we can break the loop

    if hwnd:
        # If we found a window, bring it to the foreground
        bring_to_foreground(hwnd)
    elif app_path:
        try:
            subprocess.Popen(app_path)  # Open the application if it is not running
        except Exception as e:
            print(f"ERROR: Error opening application '{app_path}': {e}")
    else:
        print(
            f"{application_name} could not be found nor is open. Please ensure it is installed and accessible via system PATH.")

    return get_active_window_title()



if __name__ == "__main__":
    # active_title = activate_windowt_title("chrome")
    active_title = activate_windowt_title("Google Chrome")
    print(f"Active window title: {active_title}")


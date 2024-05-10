import win32com.client
import win32gui
import win32con
from datetime import datetime


def enumerate_windows():
    windows = []
    top_windows = []

    def enum_window_callback(hwnd, _):
        windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    win32gui.EnumWindows(enum_window_callback, None)
    windows.sort(key=lambda x: -x[0])
    for i, (_, title) in enumerate(windows):
        if title:
            top_windows.append((title, i))
    return dict(top_windows)


def should_exclude_process(name):
    excluded_processes = ['dwm.exe', 'nvcontainer.exe', 'nvidia broadcast ui.exe', 'system', 'python.exe', 'steam.exe',
                          'TextInputHost.exe', 'pycharm64.exe', 'nvidia broadcast.exe', 'widgets.exe', 'amdow.exe',
                          'CTkToplevel', 'AI Drone Assistant', 'Ctk', 'Ctk.exe', 'tk', 'tk.exe', 'Code', 'Code.exe',
                          'NVIDIA Share.exe', 'NVIDIA Web Helper.exe', 'nvsphelper64.exe', 'NVIDIA GeForce Experience.exe',
                          'nvcontainer.exe', 'NVDisplay.Container.exe', 'widgets.exe', 'translucenttb.exe', 'securityhealthsystray.exe']
    return name in excluded_processes


def get_opened_programs():
    wmi = win32com.client.GetObject('winmgmts:')
    processes = wmi.InstancesOf('Win32_Process')
    window_order = enumerate_windows()
    process_list = []
    added_titles = set()

    for process in processes:
        try:
            name = process.Properties_('Name').Value
            pid = process.Properties_('ProcessId').Value
            creation_date = process.Properties_('CreationDate').Value
            creation_datetime = datetime.strptime(creation_date.split('.')[0], '%Y%m%d%H%M%S')

            if should_exclude_process(name):
                continue

            for title, order in window_order.items():
                if name[:-4].lower() in title.lower() and title not in added_titles:
                    process_list.append((name, pid, creation_datetime, title, order))
                    added_titles.add(title)
                    break

        except Exception as e:
            print(f"Error getting information for PID {pid}: {e}")

    process_list.sort(key=lambda x: x[4])
    return process_list


def format_programs_list():
    programs = get_opened_programs()
    output = []
    for proc in programs:
        line = f"Name: '{proc[0]}', PID: {proc[1]}, Creation Time: '{proc[2]}', Window Title: '{proc[3]}', Z-order Level: {proc[4]}"
        output.append(line)

    if output:
        last_focused_window = output[0]  # The first app in the list after sorting by Z-order
        output.insert(0, f"Last Focused Window: {last_focused_window}\n---\n")

    return "\n".join(output)


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
        win32gui.SetForegroundWindow(hwnd)
    else:
        print(f"Window with title '{title}' not found.")


def last_programs_list(focus_last_window=False):
    programs = get_opened_programs()
    output = []
    for proc in programs:
        line = f"Name: '{proc[0]}', PID: {proc[1]}, Creation Time: '{proc[2]}', Window Title: '{proc[3]}', Z-order Level: {proc[4]}"
        output.append(line)

    if programs and focus_last_window:
        last_focused_window_title = programs[0][3]  # Window title of the last focused window
        set_foreground_window_by_title(last_focused_window_title)
        output.insert(0, f"Last Focused Window: {last_focused_window_title}\n---\n")

    return "\n".join(output)


# # Example usage
# result_string = last_programs_list(focus_last_window=True)
# print(result_string)

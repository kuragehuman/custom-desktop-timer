import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
MONITOR_DEFAULTTONEAREST = 2


class MONITORINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("rcMonitor", wintypes.RECT),
        ("rcWork", wintypes.RECT),
        ("dwFlags", wintypes.DWORD),
    ]

# -----------------------------
# マウスポインタのある画面のタスクバーを除いたサイズを取得
# -----------------------------
def get_work_area():

    pt = wintypes.POINT()
    user32.GetCursorPos(ctypes.byref(pt))

    monitor = user32.MonitorFromPoint(pt, MONITOR_DEFAULTTONEAREST)

    info = MONITORINFO()
    info.cbSize = ctypes.sizeof(info)
    user32.GetMonitorInfoW(monitor, ctypes.byref(info))

    return info.rcWork

def get_all_work_areas():

    monitors = []

    def callback(hMonitor, hdcMonitor, lprcMonitor, dwData):

        info = MONITORINFO()
        info.cbSize = ctypes.sizeof(info)
        user32.GetMonitorInfoW(hMonitor, ctypes.byref(info))

        monitors.append(info.rcWork)

        return True

    MONITORENUMPROC = ctypes.WINFUNCTYPE(
        wintypes.BOOL,
        wintypes.HMONITOR,
        wintypes.HDC,
        wintypes.LPRECT,
        wintypes.LPARAM
    )

    user32.EnumDisplayMonitors(
        0,
        0,
        MONITORENUMPROC(callback),
        0
    )

    return monitors
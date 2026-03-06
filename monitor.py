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

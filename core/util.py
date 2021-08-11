from tkinter import Tk
import ctypes
import platform


def applyWindowsOptimizations(window: Tk):
    if platform.system() != "Windows":
        return
    versionString = platform.version()
    # 界面缩放仅适用于 Windows 8.1 以上版本
    if not (versionString.startswith("6.3") or versionString.startswith("10")):
        return
    # 适配高 DPI
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    window.tk.call('tk', 'scaling', factor / 75)

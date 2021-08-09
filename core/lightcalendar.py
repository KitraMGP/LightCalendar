from tkinter import Tk
from core.lightcalendar_state import LightCalendarState
from ui.main_window import MainWindow
import ctypes
import platform


class LightCalendar:
    mainWindow: MainWindow
    state: LightCalendarState

    @staticmethod
    def initialize():
        mainWindow = MainWindow()
        mainWindow.show()

    @staticmethod
    def applyWindowsOptimizations(window: Tk):
        if platform.system != "Windows":
            return
        versionString = platform.version()
        # 界面缩放仅适用于 Windows 8.1 以上版本
        if not (versionString.startswith("6.3")
                or versionString.startswith("10")):
            return
        # 适配高 DPI
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        window.tk.call('tk', 'scaling', factor / 75)

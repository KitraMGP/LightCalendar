from core.lightcalendar_state import LightCalendarState
from ui.main_window import MainWindow


class LightCalendar:
    mainWindow: MainWindow
    state: LightCalendarState

    @staticmethod
    def initialize():
        mainWindow = MainWindow()
        mainWindow.show()

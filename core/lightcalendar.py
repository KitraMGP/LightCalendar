from core.lightcalendar_state import LightCalendarState
from ui.main_window import MainWindow


class LightCalendar:
    mainWindow: MainWindow

    def initialize(self):
        self.state = LightCalendarState()
        self.mainWindow = MainWindow()
        self.mainWindow.show()

from core.lightcalendar_state import LightCalendarState
from ui.main_window import MainWindow


class LightCalendar:
    mainWindow: MainWindow
    state: LightCalendarState

    def initialize(self):
        self.state = LightCalendarState()
        self.mainWindow = MainWindow(self.state)
        self.mainWindow.show()

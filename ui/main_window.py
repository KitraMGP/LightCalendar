from datetime import datetime, timedelta
from functools import partial
import tkinter
from typing import List
from core.calendar_provider import CalendarProvider
from datetime import date
import os
from core.calendar_data import CalendarData
from core.lightcalendar_state import CalendarMode, LightCalendarState
from core.util import applyWindowsOptimizations
from tkinter import *
from tkinter.ttk import *

# 为了简化代码创建的全局变量，和 MainWindow::window 引用同一实例
_window: Tk
_weekday = ["日", "一", "二", "三", "四", "五", "六"]


def _getWeekDay(day: int) -> str:
    return "星期" + _weekday[day - 1]


class MainWindow:
    """控制 LightCalender 主窗体的整个生命周期以及其逻辑。

    必须实例化后才能使用，它被实例化的同时也会创建并显示主窗体。

    window: 主窗体的实例
    frameTodo: "待办事项"窗格
    frameToolBar: 顶部工具栏
    frameCalendar: 日历窗格
    windowWidth, windowHeight: 窗体尺寸(仅用于获取窗体尺寸)
    """

    state: LightCalendarState
    window: Tk
    frameTodo: Frame
    frameToolBar: Frame
    frameCalendar: Frame

    windowWidth: int
    windowHeight: int

    calendarData: CalendarData
    calendarMode: CalendarMode
    daySelected: date

    def __init__(self):
        self.state = LightCalendarState()
        global _window
        _window = Tk()
        applyWindowsOptimizations(_window)
        self.window = _window
        self.windowWidth = 400
        self.windowHeight = 250
        _window.title("轻日历")
        _window.iconbitmap("./assets/icon.ico")
        _window.geometry("%sx%s" % (self.windowWidth, self.windowHeight))
        _window.minsize(400, 250)
        self.frameTodo = Frame(_window, borderwidth=1, relief=SOLID)
        self.frameToolBar = Frame(_window, borderwidth=1, relief=SOLID)
        self.frameCalendar = Frame(_window, borderwidth=1, relief=SOLID)
        # 利用 place 布局方式让各控件适应窗体大小变化
        self.frameTodo.place(relx=0, rely=0, relwidth=0.25, relheight=1.00)
        self.frameToolBar.place(relx=0.25,
                                rely=0,
                                relwidth=0.75,
                                relheight=0.15)
        self.frameCalendar.place(relx=0.25,
                                 rely=0.15,
                                 relwidth=0.75,
                                 relheight=0.85)

        # frameTodo
        frameTodo_labelTop = Label(self.frameTodo, text="待办事项")
        frameTodo_labelTop.pack(side=TOP, pady=3)

        # frameCalendar frameToolBar
        self._initCalendar()

    def _initCalendar(self):
        if (os.path.exists("data.json")):
            self.calendarData = CalendarData.readFromJson("data.json")
        else:
            self.calendarData = CalendarData(dict())
            self.calendarData.writeToJson("data.json")
        self.calendarMode = CalendarMode.Month
        self.daySelected = date.today()
        self._updateMonthCalendar()

    def _updateMonthCalendar(self):
        year = self.daySelected.year
        month = self.daySelected.month
        # 工具栏的日期
        Label(self.frameToolBar,
              text=("%d 年 %d 月" % (year, month)),
              anchor=CENTER,
              justify=CENTER).place(relx=0, rely=0, relwidth=0.3, relheight=1)
        # 工具栏的按钮
        Button(self.frameToolBar, text="<-",
               command=self._prevMonth).place(relx=0.3,
                                              rely=0,
                                              relwidth=0.15,
                                              relheight=1)
        Button(self.frameToolBar, text="->",
               command=self._nextMonth).place(relx=0.45,
                                              rely=0,
                                              relwidth=0.15,
                                              relheight=1)
        Button(self.frameToolBar, text="关于…",
               command=self._openAboutDialog).place(relx=0.85,
                                                    rely=0,
                                                    relwidth=0.15,
                                                    relheight=1)
        # body
        monthCalendar = CalendarProvider.genMonthCalendar(year, month)
        dRelW = 1.0 / 7
        dRelH = 1.0 / (len(monthCalendar.calendarBody) + 1)
        curX = 0
        curY = 0
        for i in range(0, 7):
            Label(self.frameCalendar,
                  text=_getWeekDay(i + 1),
                  anchor=CENTER,
                  justify=CENTER).place(relx=curX,
                                        rely=curY,
                                        relwidth=dRelW,
                                        relheight=dRelH)
            curX += dRelW
        curY += dRelH
        for week in monthCalendar.calendarBody:
            curX = 0
            for day in week:
                d = self.daySelected
                if day.year == d.year and day.month == d.month and day.day == d.day:
                    button = tkinter.Button(self.frameCalendar,
                                            text=day.day,
                                            background="#3397ff",
                                            activebackground="#3397ff",
                                            foreground="#ffffff",
                                            activeforeground="#ffffff",
                                            relief=FLAT)
                else:
                    button = Button(
                        self.frameCalendar,
                        text=day.day,
                        # 用 functools.partial() 生成提前传入参数的函数实例
                        command=partial(self._selectDate, day.year, day.month,
                                        day.day))
                if day.isNotInThisMonth:
                    button.config(state=DISABLED)
                button.place(relx=curX,
                             rely=curY,
                             relwidth=dRelW,
                             relheight=dRelH)
                curX += dRelW
            curY += dRelH
        self.window.update()

    def _prevMonth(self):
        d = self.daySelected
        if d.month == 1:
            self.daySelected = date.replace(d, month=12, year=d.year - 1)
        else:
            self.daySelected = date.replace(d, month=d.month - 1)
        self._updateMonthCalendar()

    def _nextMonth(self):
        d = self.daySelected
        if d.month == 12:
            self.daySelected = date.replace(d, month=1, year=d.year + 1)
        else:
            self.daySelected = date.replace(d, month=d.month + 1)
        self._updateMonthCalendar()

    def _selectDate(self, year: int, month: int, day: int):
        d = self.daySelected
        self.daySelected = date.replace(d, year=year, month=month, day=day)
        self._updateMonthCalendar()

    def _openAboutDialog(self):
        pass

    def show(self):
        """
        启动窗体消息循环。

        注：此方法会阻塞程序。
        """
        self.window.mainloop()

from typing import List
from core.lightcalendar_state import CalendarDay, MonthCalendar
from datetime import datetime

_monthDay = [31, 0, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def _isLeap(year: int) -> bool:
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def _getDay(year: int, month: int, day: int) -> int:
    """获取这一天是星期几。星期日为 0。
    """
    day = datetime(year=year, month=month, day=day).weekday() + 1
    if day == 7:
        day = 0
    return day


def _getMonthDay(year: int, month: int) -> int:
    if month != 2:
        return _monthDay[month - 1]
    else:
        return 29 if _isLeap(year) else 28


def _getLastMonthDay(year: int, month: int) -> int:
    if month - 1 != 0:  # 同一年
        return _getMonthDay(year, month - 1)
    else:  # 上一年
        return _getMonthDay(year - 1, 12)


class CalendarProvider:
    """实现日历（格子）的生成算法
    """
    @staticmethod
    def genMonthCalendar(year: int, month: int) -> MonthCalendar:
        calendar = MonthCalendar()
        dayList: List[CalendarDay] = list()
        # 这个月第一天是星期几
        firstDay = _getDay(year, month, 1)
        # 这个月有多少天
        days = _getMonthDay(year, month)
        # 上个月有多少天
        lastMonthDays = _getLastMonthDay(year, month)
        # 填充第一天前面的空位
        for i in range(0, firstDay + 1):
            curDay = lastMonthDays - firstDay + i
            lastMonth = month - 1 if month - 1 != 0 else 12
            lYear = year if month - 1 != 0 else year - 1
            dayList.append(CalendarDay(lYear, lastMonth, curDay, 0, True))
        # 这个月的日期
        for i in range(1, days + 1):
            dayList.append(CalendarDay(year, month, i, 0, False))
        column = 0
        tmp: List[CalendarDay] = list()
        # 分成 7 天一行
        for day in dayList:
            if column == 7:
                column = 0
                calendar.calendarBody.append(tmp)
                tmp.clear()
            tmp.append(day)
            column += 1
        # 填充最后一天后面的空位
        if len(tmp) != 0:
            curDay = 1
            while len(tmp) != 7:
                nextMonth = month + 1 if month + 1 != 13 else 1
                nYear = year if month + 1 != 13 else year + 1
                tmp.append(CalendarDay(nYear, nextMonth, curDay, 0, True))
                curDay += 1
        calendar.calendarBody.append(tmp)
        return calendar

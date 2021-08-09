from enum import Enum
from datetime import *
from typing import List
from dataclasses import dataclass


class CalendarMode(Enum):
    Month = 0
    Year = 1


class TodoPriority(Enum):
    Unimportant = 0
    Normal = 1
    Important = 2
    Urgent = 3

    def __str__(self):
        return ["不重要", "一般", "重要", "非常重要"][self.value]


@dataclass
class TodoEntry:
    priority: TodoPriority
    content: str
    time: datetime


@dataclass
class CalendarDay:
    year: int
    month: int
    day: int
    todoCount: int
    isNotInThisMonth: bool


class MonthCalendar:
    calendarBody: List[List[CalendarDay]]


class LightCalendarState:
    mode: CalendarMode
    monthCalendar: MonthCalendar

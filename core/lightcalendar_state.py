from enum import Enum
from datetime import *
from typing import Dict, List
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

    # 序列化
    def objToDict(obj) -> Dict:
        if not isinstance(obj, TodoEntry):
            raise TypeError
        d = dict()
        d["pri"] = obj.priority.value
        d["content"] = obj.content
        d["time"] = obj.time.strftime("%Y-%m-%d %H:%M:%S")
        return d

    # 反序列化
    def dictToObj(d: Dict):
        return TodoEntry(TodoPriority[d["pri"]], d["content"],
                         datetime.strptime(d["time", "%Y-%m-%d %H:%M:%S"]))


@dataclass
class CalendarDay:
    year: int
    month: int
    day: int
    todoCount: int
    isNotInThisMonth: bool
    isSelected: bool = False


class MonthCalendar:
    calendarBody: List[List[CalendarDay]]


class LightCalendarState:
    mode: CalendarMode
    monthCalendar: MonthCalendar
    selectedDay: datetime

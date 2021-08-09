from typing import Dict, List
from core.lightcalendar_state import CalendarMode, TodoEntry
from json import *


class CalendarData:
    """该类的实例用于存储日历数据，并实现了日历数据的存储方案。

    整个日历的核心数据存储实际上存储的是待办事项。（因为其他日期
    数据都可以现场生成）

    所有待办事项存储在 todoPool 属性中。这是一个 Dict，键为年份，
    值为该年存在待办事项的月份对应的 todoPool（没有待办事项的年份键
    不存在，下文月、日也如此）；每个月份的 todoPool 包含存在待办事项
    的日对应的 todoPool；每日的 todoPool 为一个元素类型为 TodoEntry
    的 List。

    从某种角度来看，整个顶层 todoPool 实际上就是一个树。
    """
    todoPool: Dict[int, Dict[int, Dict[int, List[TodoEntry]]]]
    mode: CalendarMode

    @staticmethod
    def readFromJson(fileName: str):
        file = open(fileName, "r", encoding="utf-8")
        instance = load(file)
        file.close()
        return instance

    def writeToJson(self, fileName: str):
        file = open(fileName, "w", encoding="utf-8")
        file.write(dumps(self, sort_keys=True))
        file.close()

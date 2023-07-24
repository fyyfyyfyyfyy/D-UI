import json
from datetime import datetime

from dui.types.religion import Religion


class Event:
    def __init__(self,
                 location: str,
                 environment: str,
                 time: datetime,
                 religion: Religion = None) -> None:
        self.location = location
        self.environment = environment
        self.religion = religion if religion is not None else Religion("吃辣舒适")
        self.time = time

    def __repr__(self) -> str:
        return (
            f"  Location: {self.location}\n"
            f"  Environment: {self.environment}\n"
            f"  Time: {self.time}\n"
            f"  Religion: {self.religion}"
        )

    def __str__(self) -> str:
        event_dict = {
            "Event": {
                "Location": self.location,
                "Environment": self.environment,
                "Time": self.time.strftime("%Y-%m-%d %H:%M:%S"),
                "Religion": self.religion.to_dict()
            }
        }
        event_json = json.dumps(event_dict, ensure_ascii=False, indent=2)
        return event_json

# 测试数据
# event1 = Event("四川北路666号", "川菜馆", "吃辣舒适", "8:00pm")
# print(repr(event1))
# print(str(event1))

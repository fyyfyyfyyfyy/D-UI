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
        self.religion = religion
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
                "Religion": {
                    "desc": self.religion.__str__()
                }
            }
        }
        event_json = json.dumps(event_dict, ensure_ascii=False, indent=2)
        return event_json

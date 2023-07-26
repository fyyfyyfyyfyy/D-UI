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
        return repr(self.__dict__)

    def __str__(self) -> str:
        output_dict = {}
        output_dict['location'] = self.location
        output_dict['event'] = self.environment
        output_dict['time'] = self.time.strftime("%Y-%m-%d %H:%M:%S")
        if self.religion is not None:
            output_dict['religion'] = str(self.religion)
        return str(output_dict)

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
        output_dict['environment'] = self.environment
        output_dict['time'] = self.time.strftime("%Y-%m-%d %H:%M:%S")
        if self.religion is not None:
            output_dict['religion'] = str(self.religion)
        return str(output_dict)

    @classmethod
    def from_dict(cls, data):
        location = data['location']
        environment = data['environment']
        time = data['time']
        # time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        religion_data = data.get('religion')
        religion = Religion.from_dict(religion_data) if religion_data else None
        return cls(location, environment, time, religion)

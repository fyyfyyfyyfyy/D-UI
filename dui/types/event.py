from dui.types.religion import Religion


class Event:
    def __init__(self,
                 location: str,
                 environment: str,
                 time: str,
                 belief: Religion = None) -> None:
        self.location = location
        self.environment = environment
        self.belief = belief if belief is not None else Religion("吃辣舒适")
        self.time = time

    def __repr__(self) -> str:
        return f"Event({self.location}, {self.environment}, {self.time}, {self.belief})"

    def __str__(self) -> str:
        return (
            f"Event:\n"
            f"  Location: {self.location}\n"
            f"  Environment: {self.environment}\n"
            f"  Time: {self.time}\n"
            f"  Belief: {self.belief}"
        )


# 测试数据
# event1 = Event("四川北路666号", "川菜馆", "吃辣舒适", "8:00pm")
# print(repr(event1))
# print(str(event1))

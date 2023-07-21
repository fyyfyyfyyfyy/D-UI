from dui.types.decimalList import DecimalList


class Desire(DecimalList):
    DESIRE_COUNT: int = 29

    def __init__(self) -> None:
        super().__init__(item_count=Desire.DESIRE_COUNT)


class Emotion(DecimalList):
    def __init__(self) -> None:
        super().__init__(item_count=5)


class Feeling(DecimalList):
    def __init__(self) -> None:
        super().__init__(item_count=5)


class Person:
    def __init__(self,
                 desire: Desire,
                 emotion: Emotion = Emotion(),
                 feeling: Feeling = Feeling()) -> None:
        self._desire: Desire = desire
        self._emotion: Emotion = emotion
        self._feeling: Feeling = feeling

    def __repr__(self) -> str:
        return repr({
            'desire': self._desire
        })

    def __str__(self) -> str:
        item_lines = [f'  {k}: {v}' for k, v in self.__dict__.items()]
        return '\n'.join(["Person:"] + item_lines)

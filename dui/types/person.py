from __future__ import annotations

from dui.types.demand import Desire, Emotion, Feeling
from dui.types.event import Event


class Person:
    def __init__(self,
                 desire: Desire,
                 emotion: Emotion = Emotion(),
                 feeling: Feeling = Feeling(),
                 history: list[Event] = []) -> None:
        self._desire: Desire = desire
        self._emotion: Emotion = emotion
        self._feeling: Feeling = feeling
        self._history: list[Event] = history if history is not None else []

    def __repr__(self) -> str:
        return repr({
            'desire': self._desire
        })

    def __str__(self) -> str:
        item_lines = [f'  {k}: {v}' for k, v in self.__dict__.items()]
        return '\n'.join(["Person:"] + item_lines)

    @property
    def desire(self) -> Desire:
        return self._desire

    @property
    def emotion(self) -> Emotion:
        return self._emotion

    @property
    def feeling(self) -> Feeling:
        return self._feeling

    @property
    def history(self) -> list:
        return self._history

    def history_push(self, event):
        self._history.append(event)

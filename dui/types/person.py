from __future__ import annotations

from dui.types import Desire, Emotion, Feeling
from dui.types.decimalList import DecimalList
from dui.types.emotion import EMOTION_NAMES
from dui.types.event import Event
from dui.types.history import HistoryItem


class Person:
    def __init__(self,
                 desire: Desire,
                 emotion: Emotion = Emotion(),
                 feeling: Feeling = Feeling(),
                 history: list[HistoryItem] = []) -> None:
        self._desire: Desire = desire
        self._emotion: Emotion = emotion
        self._stable_point: Emotion = emotion
        self._feeling: Feeling = feeling
        self._history: list[HistoryItem] = history if history is not None else []

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
    def history(self) -> list[HistoryItem]:
        return self._history

    @property
    def emotion_offset(self) -> DecimalList:
        return self._emotion - self._stable_point

    def history_push(self, event: Event | HistoryItem):
        self._history.append(HistoryItem.from_event(event))

    def apply_response_change(self, response_change):
        parsed_json = response_change.get_parsed_json()
        if parsed_json:
            for emotion_name in EMOTION_NAMES:
                if emotion_name in parsed_json:
                    new_value = parsed_json[emotion_name]
                    current_value = self._emotion.get_emotion_value(emotion_name)
                    self._emotion.set_emotion_value(emotion_name,
                                                    current_value + new_value)

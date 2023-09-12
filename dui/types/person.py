from __future__ import annotations

import math
from decimal import Decimal

from dui.types import Desire, Emotion, Feeling
from dui.types.decimalList import DecimalList
from dui.types.emotion import EMOTION_NAMES
from dui.types.event import Event
from dui.types.history import HistoryItem
from dui.types.response_change import ResponseChange
from dui.utils.log import get_logger

logger = get_logger("person", console_level="DEBUG")


class Person:
    def __init__(
        self,
        desire: Desire,
        emotion: Emotion = Emotion(),
        feeling: Feeling = Feeling(),
        history: list[HistoryItem] = [],
    ) -> None:
        self._desire: Desire = desire
        self._emotion: Emotion = emotion
        self._stable_point: Emotion = emotion
        self._feeling: Feeling = feeling
        self._history: list[HistoryItem] = history if history is not None else []

        for hi in self._history:
            logger.info(f"process {hi}")
            self._apply_change(hi)

    def __repr__(self) -> str:
        return repr({"desire": self._desire})

    def __str__(self) -> str:
        item_lines = [f"  {k}: {v}" for k, v in self.__dict__.items()]
        return "\n".join(["Person:"] + item_lines)

    def _apply_change(self, hi: HistoryItem):
        result = self._emotion + hi.impact_feeling * 0.1
        logger.debug(
            f"emotion = {self._emotion} + 0.1 * {hi.impact_feeling} = {result}"
        )
        self._emotion = result

        k = 1 if hi.impact_feeling.is_positive else -1

        desire_id = hi.religion._desire_id
        strength = hi.impact_feeling.intensity
        if desire_id not in self._desire._id2nodes:
            logger.warning(
                f"desire [{desire_id}] {hi.religion._desire_name} not found."
            )
            return None

        desire_node = self._desire._id2nodes[desire_id]
        result = desire_node.value + Decimal(k * math.sqrt(strength))
        logger.debug(
            f"desire [{desire_node.id}] {desire_node.name}"
            + f" = {desire_node.value} (before)"
            + f" + {k} * sqrt(feeling = {strength})"
            + f" = {result}"
        )
        desire_node._value = result

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

    def apply_response_change(self, response_change: ResponseChange):
        parsed_json = response_change.get_parsed_json()
        if parsed_json:
            for emotion_name in EMOTION_NAMES:
                if emotion_name in parsed_json:
                    new_value = parsed_json[emotion_name]
                    current_value = self._emotion.get_emotion_value(emotion_name)
                    self._emotion.set_emotion_value(
                        emotion_name, current_value + new_value
                    )

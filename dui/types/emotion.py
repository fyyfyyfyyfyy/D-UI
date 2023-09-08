from decimal import Decimal

from dui.types.decimalList import DecimalList

EMOTION_NAMES_CN = ['开心', '难过', '讨厌', '惊讶', '生气']
EMOTION_NAMES = ['happy', 'sad', 'hate', 'amazed', 'angry']


class Emotion(DecimalList):
    def __init__(self, **kwargs) -> None:
        super().__init__(item_count=5, item_names=EMOTION_NAMES, **kwargs)
        self._max_value = 500

    @property
    def intensity(self) -> Decimal:
        prod: Decimal = Decimal(1)
        for i in range(len(self._value) - 1):
            prod = prod * self._value[i + 1]

        return sum(self._value[1:]) / \
            (1 + prod / pow(self._max_value, len(self._value) - 1))

    @property
    def is_positive(self) -> bool:
        positive_value: Decimal = self.get_emotion_value('happy')
        negative_value: list[Decimal] = [self.get_emotion_value(i)
                                         for i in EMOTION_NAMES if i != 'happy']
        return positive_value >= sum(negative_value)

    def get_emotion_value(self, emotion_name: str) -> Decimal:
        return self[EMOTION_NAMES.index(emotion_name) + 1]

    def set_emotion_value(self, emotion_name: str, value: Decimal):
        self[EMOTION_NAMES.index(emotion_name) + 1] = value

    @classmethod
    def from_dict(cls, data):
        emotion = cls()
        for emotion_name, value in data.items():
            emotion.set_emotion_value(emotion_name, Decimal(value))
        return emotion


class Feeling(DecimalList):
    def __init__(self, **kwargs) -> None:
        super().__init__(item_count=5, item_names=EMOTION_NAMES, **kwargs)

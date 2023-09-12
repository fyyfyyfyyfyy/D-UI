from decimal import Decimal

from dui.types.decimalList import DecimalList

EMOTION_NAMES_CN = ["开心", "难过", "讨厌", "惊讶", "生气"]
EMOTION_NAMES = ["happy", "sad", "hate", "amazed", "angry"]


class EmotionBase(DecimalList):
    def __init__(self, **kwargs) -> None:
        super().__init__(item_count=5, item_names=EMOTION_NAMES, **kwargs)
        self._max_value = 500

    @property
    def intensity(self) -> Decimal:
        prod: Decimal = Decimal(1)
        for i in range(len(self._value) - 1):
            prod = prod * self._value[i + 1]

        return sum(self._value[1:]) / (
            1 + prod / pow(self._max_value, len(self._value) - 1)
        )

    @property
    def is_positive(self) -> bool:
        EH_NAME = "happy"
        positive_value: Decimal = self.get_value_by_name(EH_NAME)
        negative_value: list[Decimal] = [
            self.get_value_by_name(i) for i in EMOTION_NAMES if i != EH_NAME
        ]
        return positive_value >= sum(negative_value)

    def get_value_by_name(self, name: str) -> Decimal:
        return self[EMOTION_NAMES.index(name) + 1]

    def set_value_by_name(self, name: str, value: Decimal):
        self[EMOTION_NAMES.index(name) + 1] = value

    def __repr__(self):
        return repr(dict(zip(EMOTION_NAMES, self._value[1:])))

    @classmethod
    def from_dict(cls, data: dict) -> "EmotionBase":
        base = cls()
        for en, value in data.items():
            base.set_value_by_name(en, Decimal(value))
        return base


class Emotion(EmotionBase):
    def get_emotion_value(self, emotion_name: str) -> Decimal:
        return self.get_value_by_name(emotion_name)

    def set_emotion_value(self, emotion_name: str, value: Decimal):
        self.set_value_by_name(emotion_name, value)

    @classmethod
    def from_dict(cls, data: dict) -> "Emotion":
        emotion = cls()
        for emotion_name, value in data.items():
            emotion.set_emotion_value(emotion_name, Decimal(value))
        return emotion

    def __repr__(self):
        return super().__repr__()

    # TODO: fix emotion binary operation
    # def __add__(self, rhs: 'EmotionBase') -> 'Emotion':
    #     result = Emotion()
    #     for n in EMOTION_NAMES:
    #         result.set_emotion_value(n,
    #               self.get_value_by_name(n) + rhs.get_value_by_name(n))
    #     return result


class Feeling(EmotionBase):
    def get_feeling_value(self, feeling_name: str) -> Decimal:
        return self.get_value_by_name(feeling_name)

    def set_feeling_value(self, feeling_name: str, value: Decimal):
        self.set_value_by_name(feeling_name, value)

    @classmethod
    def from_dict(cls, data: dict) -> "Feeling":
        feeling = cls()
        for feeling_name, value in data.items():
            feeling.set_feeling_value(feeling_name, Decimal(value))
        return feeling

    def __repr__(self):
        return super().__repr__()

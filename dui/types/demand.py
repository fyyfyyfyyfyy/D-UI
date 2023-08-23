from decimal import Decimal

from dui.types.decimalList import DecimalList
from dui.utils.math import clamp


class Desire(DecimalList):
    DESIRE_COUNT: int = 29
    DESIRE_NAMES = ['rest', 'sleep', 'eating', 'drinking', 'living', 'dying',
                    'achieving self-fulfillment', 'realizing self-meaning', 'awakening',
                    'curiosity', 'thinking', 'learning', 'giving', 'pleasing oneself',
                    'gaining honor', 'gaining success', 'possession', 'gaining power',
                    'buying', 'collecting', 'getting money', 'sensory aesthetics',
                    'auditory aesthetics', 'visual aesthetics',
                    'love', 'family affection',
                    'friendship', 'psychosexual desire', 'physiological sexual desire']

    def __init__(self, **kwargs) -> None:
        super().__init__(item_count=Desire.DESIRE_COUNT, **kwargs)

    def __setitem__(self, key: int, value: Decimal | int | float):
        assert key >= 0 and key < len(self._value)
        dec_value = Decimal(value)
        self._value[key] = dec_value

    @property
    def second_layer(self):
        ml = lambda x: 3 if x in range(5, 8) else 2  # mapping lenghth
        mp = lambda x: -1 + 2 * x + clamp(x - 5, 0, 3)  # mapping start position
        me = lambda x: mp(x) + ml(x)  # mapping end

        return [0] + [max(self._value[mp(i):me(i)]) for i in range(1, 13 + 1)]

    @property
    def first_layer(self):
        ml = lambda x: 5 if x in range(2, 3) else 4  # mapping lenghth
        mp = lambda x: -3 + 4 * x + clamp(x - 2, 0, 1)  # mapping start position
        me = lambda x: mp(x) + ml(x)  # mapping end

        return [0] + [max(self.second_layer[mp(i):me(i)]) for i in range(1, 3 + 1)]


EMOTION_NAMES_CN = ['开心', '难过', '讨厌', '惊讶', '生气']
EMOTION_NAMES = ['happy', 'sad', 'hate', 'amazed', 'angry']


class Emotion(DecimalList):
    def __init__(self, **kwargs) -> None:
        super().__init__(item_count=5, item_names=EMOTION_NAMES, **kwargs)
        self._max_value = 500

    @property
    def intensity(self):
        prod = 1
        for i in range(len(self._value) - 1):
            prod = prod * self._value[i + 1]

        return sum(self._value[1:]) / \
            (1 + prod / pow(self._max_value, len(self._value) - 1))

    def get_emotion_value(self, emotion_name: str) -> Decimal:
        return self[EMOTION_NAMES.index(emotion_name)]

    def set_emotion_value(self, emotion_name: str, value: Decimal):
        self[EMOTION_NAMES.index(emotion_name)] = value


class Feeling(DecimalList):
    def __init__(self, **kwargs) -> None:
        super().__init__(item_count=5, item_names=EMOTION_NAMES, **kwargs)

from decimal import Decimal

from dui.types.decimalList import DecimalList
from dui.utils.math import clamp


class Desire(DecimalList):
    DESIRE_COUNT: int = 29

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


class Feeling(DecimalList):
    def __init__(self, **kwargs) -> None:
        super().__init__(item_count=5, item_names=EMOTION_NAMES, **kwargs)


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


if __name__ == '__main__':
    desire = Desire()
    desire[1] = 1
    desire[2] = 1.5
    desire[29] = 2
    print("第二层 [1] is ", desire.second_layer[1])
    print("第一层 [1] is ", desire.first_layer[1])
    print("第一层 [3] is ", desire.first_layer[3])

    # 测试加减乘除
    emotion1 = Emotion()
    print(type(emotion1._value))
    for i in range(1, 6):
        emotion1[i] = i + 1

    emotion2 = Emotion()
    for i in range(1, 6):
        emotion2[i] = i + 2
    print(emotion1._value)
    print(emotion2._value)
    print(emotion1 + emotion2)
    print(emotion2 - emotion1)
    print(emotion1 * 2.2)

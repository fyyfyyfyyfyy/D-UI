from decimal import Decimal

from dui.types.decimalList import DecimalList


class Desire(DecimalList):
    DESIRE_COUNT: int = 29

    def __init__(self) -> None:
        super().__init__(item_count=Desire.DESIRE_COUNT)

    def __setitem__(self, key: int, value: Decimal | int | float):
        assert key >= 0 and key < len(self._value)
        dec_value = Decimal(value)
        self._value[key] = dec_value
        print(f"set _value[{key}] = {self._value[key]}")

    @property
    def second_layer(self):
        second_layer = [Decimal(0) for _ in range(13 + 1)]
        for i in range(1, 14):
            if (i in [1, 2, 3, 4]):
                second_layer[i] = max(
                    self._value[2 * i - 1], self._value[2 * i])
            elif (i in [5, 6, 7]):
                second_layer[5] = max(self._value[9],
                                      self._value[10], self._value[11])
                second_layer[6] = max(self._value[12],
                                      self._value[13], self._value[14])
                second_layer[7] = max(self._value[15],
                                      self._value[16], self._value[17])
            else:
                second_layer[i] = max(self._value[2 * i + 2],
                                      self._value[2 * i + 3])
        return second_layer

    @property
    def first_layer(self):
        first_layer = [Decimal(0) for _ in range(3 + 1)]
        first_layer[1] = max(self.second_layer[1], self.second_layer[2],
                             self.second_layer[3], self.second_layer[4])
        first_layer[2] = max(self.second_layer[5], self.second_layer[6],
                             self.second_layer[7], self.second_layer[8],
                             self.second_layer[9])
        first_layer[3] = max(self.second_layer[10], self.second_layer[11],
                             self.second_layer[12], self.second_layer[13])
        return first_layer


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
        re_format = dict()  # 对dict中的数据去除decimal创建字典存储
        for k, v in self.__dict__.items():
            v = dict(v)
            re_format[k] = {key: eval(value.__str__())
                            for key, value in v.items()}
        item_lines = [f'  {k}: {dict(v)}' for k, v in re_format.items()]
        return '\n'.join(["Person:"] + item_lines)

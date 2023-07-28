from dui.types.demand import Desire, Emotion, Feeling
from dui.types.event import Event


class Person:
    def __init__(self,
                 desire: Desire,
                 emotion: Emotion = Emotion(),
                 feeling: Feeling = Feeling(),
                 history=None) -> None:
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
    def desire(self):
        return self._desire

    @property
    def emotion(self):
        return self._emotion

    @property
    def feeling(self):
        return self._feeling

    @property
    def history(self):
        return self._history

    def history_push(self, event):
        self._history.append(event)


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

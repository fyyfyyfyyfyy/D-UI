from collections.abc import MutableMapping
from decimal import Decimal


class Desire(MutableMapping):
    def __init__(self) -> None:
        self._value: list[Decimal] = [Decimal(0) for _ in range(30)]

    def __getitem__(self, key: int) -> Decimal:
        return self._value[key]

    def __setitem__(self, key: int, value: Decimal | int):
        assert key >= 0 and key < len(self._value)
        dec_value = Decimal(value)
        self._value[key] = dec_value

    def __delitem__(self, key: int):
        del self._value[key]

    def __iter__(self):
        return iter(range(len(self._value)))

    def __len__(self) -> int:
        return len(self._value)

    def __repr__(self):
        return repr(dict(enumerate(self._value)))


class Person:
    def __init__(self, desire: Desire) -> None:
        self._desire: Desire = desire
        pass

    def __repr__(self) -> str:
        return repr({
            'desire': self._desire
        })

    def __str__(self) -> str:
        item_lines = [f'  {k}: {v}' for k, v in self.__dict__.items()]
        return '\n'.join(["Person:"] + item_lines)

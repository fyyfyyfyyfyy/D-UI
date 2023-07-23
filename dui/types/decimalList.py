from collections.abc import MutableMapping
from decimal import Decimal
from typing import Any


class DecimalList(MutableMapping):
    def __init__(self, item_count: int) -> None:
        self.class_name = self.__class__.__name__
        self._item_count = item_count
        self._value: list[Decimal] = [
            Decimal(0) for _ in range(self._item_count + 1)]

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

    def __add__(self, add_nums: Any) -> Any:
        return [add1 + add2 for add1, add2
                in zip(self._value, add_nums._value)]

    def __sub__(self, sub_nums: Any) -> Any:
        return [sub1 - sub2 for sub1, sub2
                in zip(self._value, sub_nums._value)]

    def __mul__(self, ep: int | Decimal | float):
        ep = Decimal(ep)
        return [item * ep for item in self._value]

    def __div__(self, ep: int | Decimal | float):
        ep = Decimal(ep)
        return [item / ep for item in self._value]

    def __str__(self) -> str:
        items = dict([(i, str(v)) for (i, v) in enumerate(self._value)])
        items_str = ', '.join([f'{i}: {v}' for i, v in items.items()])
        return '{' + items_str + '}'

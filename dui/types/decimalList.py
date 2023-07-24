from collections.abc import MutableMapping
from decimal import Decimal
from typing import Any


class DecimalList(MutableMapping):
    def __init__(self, item_count: int, item_values: Any = None) -> None:
        self._item_count = item_count
        self._value: list[Decimal] = [
            Decimal(0) for _ in range(self._item_count + 1)]
        if item_values is not None:
            for i in range(len(item_values)):
                li = i + 1
                if li >= 1 and li < self._item_count:
                    self._value[li] = Decimal(item_values[i])

    def __getitem__(self, key: int) -> Decimal:
        return self._value[key]

    def __setitem__(self, key: int, value: Decimal | int | float):
        assert key >= 0 and key < len(self._value)
        dec_value = Decimal(value)
        self._value[key] = dec_value

    def __delitem__(self, key: int):
        del self._value[key]

    def __iter__(self):
        return iter(self._value)

    def __len__(self) -> int:
        return len(self._value)

    def __repr__(self):
        items = dict([(i, str(v)) for (i, v) in enumerate(self._value)])
        items_str = ', '.join([f'{i}: {v}' for i, v in items.items()])
        return '{' + items_str + '}'

    def __add__(self, rhs: Any) -> Any:
        values = [iv + r for (iv, r) in zip(self._value, rhs)]
        return DecimalList(self._item_count, values)

    def __sub__(self, rhs: Any) -> Any:
        values = [iv - r for (iv, r) in zip(self._value, rhs)]
        return DecimalList(self._item_count, values)

    def __mul__(self, rhs: Decimal | int | float):
        values = [item * Decimal(rhs) for item in self._value]
        return DecimalList(self._item_count, values)

    def __div__(self, rhs: Decimal | int | float):
        values = [item / Decimal(rhs) for item in self._value]
        return DecimalList(self._item_count, values)

from __future__ import annotations

from collections.abc import MutableMapping
from decimal import Decimal
from typing import Any, Sequence


class DecimalList(MutableMapping):
    def __init__(self, item_count: int,
                 item_values: Sequence | None = None,
                 item_names: Sequence | None = None,
                 raw_data_flag: bool = False,
                 raw_disp_flag: bool | None = None) -> None:
        self._item_count = item_count
        self._value: list[Decimal] = [
            Decimal(0) for _ in range(self._item_count + 1)]
        self._item_names = {}
        self._raw_data_flag = raw_data_flag or False
        self._raw_disp_flag = raw_disp_flag or self._raw_data_flag

        remap_offset = 0 if raw_data_flag else 1

        if item_values is not None:
            map_range = min(item_count + 1, len(item_values))
            for i in range(map_range):
                self._value[i + remap_offset] = Decimal(item_values[i])

        if item_names is not None:
            map_range_2 = min(item_count + 1, len(item_names))
            for i in range(map_range_2):
                self._item_names[i + remap_offset] = item_names[i]

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
        start_i = 1 if self._raw_disp_flag else 0  # modify the logical relationship
        items = dict([(i, str(v)) for (i, v) in enumerate(self._value) if i >= start_i])
        items_str = ', '.join([f'{self._item_names.get(i, str(i))}: {v}'
                               for i, v in items.items()])
        return '{' + items_str + '}'

    def __add__(self, rhs: Any) -> Any:
        values = [iv + r for (iv, r) in zip(self._value, rhs)]
        return DecimalList(self._item_count, values, raw_data_flag=True)

    def __sub__(self, rhs: Any) -> Any:
        values = [iv - r for (iv, r) in zip(self._value, rhs)]
        return DecimalList(self._item_count, values, raw_data_flag=True)

    def __mul__(self, rhs: Decimal | int | float):
        values = [item * Decimal(rhs) for item in self._value]
        return DecimalList(self._item_count, values, raw_data_flag=True)

    def __truediv__(self, rhs: Decimal | int | float):  # use truediv instead of __div__
        values = [item / Decimal(rhs) for item in self._value]
        return DecimalList(self._item_count, values, raw_data_flag=True)

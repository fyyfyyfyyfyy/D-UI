from collections.abc import MutableMapping
from decimal import Decimal


class DecimalList(MutableMapping):
    def __init__(self, item_count: int) -> None:
        self._item_count = item_count
        self._value: list[Decimal] = [Decimal(0) for _ in range(self._item_count + 1)]

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

from decimal import Decimal

from dui.types.decimalList import DecimalList
from dui.types.demand import Desire, Feeling


class DesireWeight(DecimalList):
    DESIRE_COUNT: int = 29

    def __init__(self) -> None:
        super().__init__(item_count=Desire.DESIRE_COUNT)


class Religion:
    def __init__(self,
                 desc: str,
                 feeling: Feeling = Feeling(),
                 desire_weight: DesireWeight = DesireWeight()) -> None:
        self._description: str = desc
        self._feeling: Feeling = feeling
        self._desire_weight: DesireWeight = desire_weight

    def __str__(self) -> str:
        return self._description

    def get_related_strength(self, desire: Desire) -> Decimal:
        total_desire = Decimal(0)
        for s_desire_weight, s_desire in zip(self._desire_weight, desire._value):
            s_res = s_desire * s_desire_weight
            total_desire = total_desire + s_res
        return total_desire

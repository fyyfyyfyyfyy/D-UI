from decimal import Decimal
from typing import Optional

from dui.types import Desire, Feeling
from dui.types.decimalList import DecimalList


class DesireWeight(DecimalList):
    DESIRE_COUNT: int = 29

    def __init__(self) -> None:
        super().__init__(item_count=Desire.DESIRE_COUNT)


class Religion:
    def __init__(self,
                 desc: str = "放下自我去享受此刻",
                 primer: str = "我相信/认为",
                 desire_name: Optional[str] = None,
                 middle_word: str = "是",
                 valence: bool = True,
                 feeling: Feeling = Feeling(),
                 desire: Desire = Desire(),
                 desire_weight: DesireWeight = DesireWeight()) -> None:
        id = desire.get_id_by_name(desire_name)
        if id is None:
            raise ValueError(f"desire_name {desire_name} does not exist")
        self._desire_id = id
        self._description: str = desc
        self._feeling: Feeling = feeling
        self._desire_weight: DesireWeight = desire_weight
        self._primer: str = primer
        self._desire_name: Optional[str] = desire_name
        self._middle_word: str = middle_word
        self._valence: int = valence

    def __str__(self) -> str:
        return self._description

    @property
    def valence(self) -> str:
        '''
        todo: add determining factor
        '''
        if (self._valence):
            return "无我"
        return "有我"

    def get_related_strength(self, desire: Desire) -> Decimal:
        total_desire = Decimal(0)
        for s_desire_weight, s_desire in zip(self._desire_weight, desire.third_layer):
            s_res = s_desire * s_desire_weight
            total_desire = total_desire + s_res
        return total_desire

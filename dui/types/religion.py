from decimal import Decimal
from typing import Optional

from dui.types import Feeling
from dui.types.decimalList import DecimalList
from dui.types.desire import Desire, DesireItem
from dui.utils.data import load_data

RELIGION_CONTENT = load_data("religion")


class DesireWeight(DecimalList):
    DESIRE_COUNT: int = 29

    def __init__(self) -> None:
        super().__init__(item_count=Desire.DESIRE_COUNT)


class Religion:
    def __init__(self,
                 desc: str = "放下自我去享受此刻",
                 primer: str = "我相信/认为",
                 desire_name: Optional[str] = None,
                 desire_item: DesireItem = None,
                 middle_word: str = "是",
                 valence: bool = True,
                 feeling: Feeling = Feeling(),
                 desire: Desire = Desire(),
                 root_id: str = "DN",
                 desire_weight: DesireWeight = DesireWeight()) -> None:
        if desire_item is None and desire_name is None:
            raise ValueError("Neither 'desire_item' nor 'desire_name'")
        if desire_item is None:
            id = desire.get_id_by_name(desire_name)
            if id is None:
                raise ValueError("the desire_item does not exist")
            desire_item = desire._all_nodes[id]
        else:
            id = desire_item.id
            try:
                desire_item = desire._all_nodes[id]
            except Exception:
                raise ValueError("The id of DesireItem WRONG!")

        self._desire_name: Optional[str] = desire_item.name
        self._desire_id = id
        self._feeling: Feeling = feeling
        self._desire_weight: DesireWeight = desire_weight

        while (desire_item is not None and desire_item.id not in ["DN", "DS", "DD"]):
            desire_item = desire_item.parent
        root_id = desire_item.id if desire_item is not None else "DN"
        for description in RELIGION_CONTENT['religion']:
            if root_id == description['id']:
                self._root_id = root_id
                primer = description['primer']
                middle_word = description['middle_word']
                if valence:
                    valence_str = description['valence'][1]
                else:
                    valence_str = description['valence'][0]
                desc = primer + self._desire_name + middle_word + valence_str
        self._primer: str = primer
        self._middle_word: str = middle_word
        self._description: str = desc
        self._valence: int = valence
        self._valence_str = valence_str

    def __str__(self) -> str:
        return self._description

    @property
    def valence(self) -> str:
        return self._valence_str

    def get_related_strength(self, desire: Desire) -> Decimal:
        total_desire = Decimal(0)
        for s_desire_weight, s_desire in zip(self._desire_weight, desire.third_layer):
            s_res = s_desire * s_desire_weight
            total_desire = total_desire + s_res
        return total_desire

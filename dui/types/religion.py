from decimal import Decimal

from dui.types import Feeling
from dui.types.decimalList import DecimalList
from dui.types.desire import Desire, DesireItem
from dui.utils.data import load_data

RELIGION_CONTENT = load_data("religion")
RELIGION_DICT = dict([(i["id"], i) for i in RELIGION_CONTENT['religion']])


class DesireWeight(DecimalList):
    DESIRE_COUNT: int = 29

    def __init__(self) -> None:
        super().__init__(item_count=Desire.DESIRE_COUNT)


class Religion:
    def __init__(self,
                 desc: str = "放下自我去享受此刻",
                 desire_name: str | None = None,
                 desire_item: DesireItem = None,
                 valence: bool = True,
                 feeling: Feeling = Feeling(),
                 desire: Desire = Desire(),
                 desire_weight: DesireWeight = DesireWeight()) -> None:
        if desire_item is None and desire_name is None:
            raise ValueError("Neither 'desire_item' nor 'desire_name' is None")

        if desire_item is None and desire_name is not None:
            desire_item = desire.get_item_by_name(desire_name)

        assert desire_item is not None, "desire_item is None"

        self._desire_id = desire_item.id
        self._desire_name = desire_item.name

        self._feeling: Feeling = feeling
        self._desire_weight: DesireWeight = desire_weight

        while (desire_item is not None and desire_item.id not in ["DN", "DS", "DD"]):
            desire_item = desire_item.parent

        self._root_id = desire_item.id if desire_item is not None else "DN"
        religion_item = RELIGION_DICT[self._root_id]

        self._primer: str = religion_item['primer']
        self._middle_word: str = religion_item['middle_word']
        self._valence: bool = valence
        self._valence_str = religion_item['valence'][1 if self._valence else 0]

        self._description: str = "".join([
            self._primer,
            self._desire_name,
            self._middle_word,
            self._valence_str])

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

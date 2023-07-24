from dui.types.person import DecimalList, Desire, Feeling


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

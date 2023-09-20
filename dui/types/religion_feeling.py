import typing

from dui.types.desire import DESIRE_PROPERTY, DesireItem
from dui.types.emotion import Feeling
from dui.types.religion import Religion
from dui.utils.data import load_data
from dui.utils.log import get_logger

logger = get_logger("religion_effect")


class ReligionEffect:
    def __init__(
        self,
        desire_id: str,
        desire_name: str,
        positive_feelings: Feeling = Feeling(),
        negative_feelings: Feeling = Feeling(),
    ) -> None:
        self.desire_id: str = desire_id
        self.desire_name: str = desire_name
        self.positive_effect: Feeling = positive_feelings
        self.negative_effect: Feeling = negative_feelings


def _data_item_to_religion_effect(data: dict[str, typing.Any]) -> ReligionEffect:
    d_id = data["id"]
    d_name = data["name"]
    d_positive_effect = data.get("positive_effect", {})
    d_negative_effect = data.get("negative_effect", {})

    d_p_feeling = Feeling.from_dict(d_positive_effect)
    d_n_feeling = Feeling.from_dict(d_negative_effect)

    desire_item: DesireItem = DESIRE_PROPERTY._id2nodes[d_id]

    if d_name != desire_item.name:
        logger.warn(
            "invalid desire name in religion-effect: "
            f"[{d_id}] {d_name}, expected name is [{desire_item.name}]"
        )

    r = ReligionEffect(
        desire_id=d_id,
        desire_name=d_name,
        positive_feelings=d_p_feeling,
        negative_feelings=d_n_feeling,
    )

    return r


def _data_to_religion_effect_mapping(data: list[dict]) -> dict[str, ReligionEffect]:
    religion_effects = [_data_item_to_religion_effect(d) for d in RELIGION2FEELING_DATA]
    mapping = [(re.desire_id, re) for re in religion_effects]
    return dict(mapping)


RELIGION2FEELING_DATA = load_data("religion_effect")

RELIGION_EFFECTS = _data_to_religion_effect_mapping(RELIGION2FEELING_DATA)


def map_religion_feeling(religion: Religion) -> Feeling:
    if religion._desire_id in RELIGION_EFFECTS:
        effect = RELIGION_EFFECTS[religion._desire_id]
        if religion._valence:
            return effect.positive_effect
        else:
            return effect.negative_effect
    else:
        logger.warn(
            'Failed to map religion of Desire '
            f'[{religion._desire_id}] "{religion._desire_name}" to feeling'
        )
        return Feeling()

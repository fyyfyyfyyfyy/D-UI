import sys

sys.path.append(".")
import typing

import yaml

from dui.types.emotion import EMOTION_NAMES


def feelings_list2dict(feelings: list[int]) -> dict[str, int]:
    return {EMOTION_NAMES[i]: f for i, f in enumerate(feelings) if f > 0}


class ReligionEffect:
    def __init__(
        self,
        id: str,
        name: str,
        positive_feelings: list[int],
        negative_feelings: list[int],
    ) -> None:
        self.id = id
        self.name = name
        self.positive_feelings = positive_feelings
        self.negative_feelings = negative_feelings

    def to_dict(self) -> dict:
        positive_effect = feelings_list2dict(self.positive_feelings)
        negative_effect = feelings_list2dict(self.negative_feelings)
        target: dict[str, typing.Any] = {
            "id": self.id,
            "name": self.name,
        }
        if len(positive_effect) > 0:
            target["positive_effect"] = positive_effect
        if len(negative_effect) > 0:
            target["negative_effect"] = negative_effect
        return target


def parseInt(v: str, default: int = 0) -> int:
    try:
        return int(v)
    except ValueError:
        return default


def process_data(data) -> list[ReligionEffect]:
    lines = data.strip().split("\n")
    output: list[ReligionEffect] = []

    for line in lines:
        parts = line.split("\t")
        assert len(parts) == 2 + 2 * 5

        p_id, p_name = parts[:2]
        positive_feelings = [parseInt(v) for v in parts[2:7]]
        negative_feelings = [parseInt(v) for v in parts[7:12]]

        item = ReligionEffect(p_id, p_name, positive_feelings, negative_feelings)

        output.append(item)

    return output


if __name__ == "__main__":
    with open("utils/religion_effect.tsv", "r", encoding="utf-8") as f:
        raw_data = f.read()

    effects = process_data(raw_data)
    # print(yaml_output)

    with open("utils/religion_effect.yml", "w") as f:
        yaml.dump(
            [e.to_dict() for e in effects],
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )

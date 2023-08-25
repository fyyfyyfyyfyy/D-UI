import copy
import typing
from decimal import Decimal

from dui.utils.data import load_data


class DesireItem:
    def __init__(
        self,
        id: str,
        name: str,
        code: str,
        level: int,
        items: list["DesireItem"] = None,
        parent: "DesireItem" = None,
        value: Decimal = None,
    ) -> None:
        self.code = code
        self.level = level
        self.id = id
        self.name = name
        self.items = items if items is not None else []
        self.parent = parent
        self._value: Decimal = Decimal(value) if value is not None else Decimal(0)

    def to_dict(self) -> dict:
        target: dict[str, typing.Any] = {
            "id": self.id,
            "name": self.name,
            "code": self.code,
        }
        if len(self.items) > 0:
            target["items"] = [item.to_dict() for item in self.items]

        return target

    @property
    def value(self) -> Decimal:
        child_max = max([item.value for item in self.items], default=0)
        return max(self._value, Decimal(child_max))


def _dict_to_desire_item(data: dict[str, typing.Any], level: int) -> DesireItem:
    items = [_dict_to_desire_item(item, level + 1) for item in data.get("items", [])]
    parent = DesireItem(data["id"], data["name"], data["code"], level, items)
    for i in items:
        i.parent = parent
    return parent


def _data_to_desire_tree(data: list[typing.Any]) -> DesireItem:
    items = [_dict_to_desire_item(item, 1) for item in data]
    root = DesireItem("DROOT", "ROOT", "RL0", 0, items)
    for i in items:
        i.parent = root
    return root


DESIRE_PROPERTY: DesireItem = _data_to_desire_tree(load_data("desire"))

DESIRE_ID_TO_NAME: dict[str, str] = load_data("desire_name")


class Desire:
    DESIRE_COUNT = 29

    def __init__(self) -> None:
        self.root = copy.deepcopy(DESIRE_PROPERTY)
        self._node_layers: list[dict[str, DesireItem]] = []
        self._build_node_layers()
        self._all_nodes: dict[str, DesireItem] = {}
        self._build_node_dict()

    def _build_node_layers(self):
        self._node_layers = [{self.root.id: self.root}]
        layer: dict[str, DesireItem] = dict([(i.id, i) for i in self.root.items])

        while len(layer) > 0:
            self._node_layers.append(layer)
            layer = dict(
                [(i.id, i) for n in self._node_layers[-1].values() for i in n.items]
            )

    def _build_node_dict(self):
        self._all_nodes = {}
        for layer in self._node_layers:
            for node in layer.values():
                self._all_nodes[node.id] = node

    @property
    def first_layer(self):
        ids = ["DN", "DS", "DD"]
        return [0] + [self._all_nodes[i].value for i in ids]

    @property
    def second_layer(self):
        base = [("DN", 4), ("DS", 5), ("DD", 4)]
        node_ids = [
            f"{prefix}{i}" for prefix, count in base for i in range(1, count + 1)
        ]
        return [0] + [self._all_nodes[i].value for i in node_ids]

    @property
    def third_layer(self):
        return [0] + [
            self._all_nodes[f"D{i}"].value for i in range(1, Desire.DESIRE_COUNT + 1)
        ]

    @third_layer.setter
    def third_layer(self, value: list):
        for i, v in enumerate(value):
            self._all_nodes[f"D{i}"]._value = Decimal(v)

    def __setitem__(self, key: int, value: Decimal | int | float):
        assert key > 0 and key <= Desire.DESIRE_COUNT
        dec_value = Decimal(value)
        self._all_nodes[f"D{key}"]._value = dec_value

    def __repr__(self) -> str:
        third_layer_node = [self._all_nodes[f"D{i}"] for i in range(1, 30)]
        valid_nodes = dict(
            [(i.name, int(i.value)) for i in third_layer_node if i.value > 0]
        )
        return repr(valid_nodes)


"""
'rest', 'sleep', 'eating', 'drinking', 'living', 'dying',
'achieving self-fulfillment', 'realizing self-meaning', 'awakening',
'curiosity', 'thinking', 'learning', 'giving', 'pleasing oneself',
'gaining honor', 'gaining success', 'possession', 'gaining power',
'buying', 'collecting', 'getting money', 'sensory aesthetics',
'auditory aesthetics', 'visual aesthetics',
'love', 'family affection',
'friendship', 'psychosexual desire', 'physiological sexual desire'
"""

import copy
import typing
from decimal import Decimal

from dui.utils.data import load_data
from dui.utils.log import get_logger

logger = get_logger("desire")


class DesireItem:
    def __init__(
        self,
        id: str,
        name: str,
        code: str,
        level: int,
        items: list["DesireItem"] = None,
        parent: "DesireItem" = None,
        value: Decimal | int | float | None = None,
    ) -> None:
        self.code = code
        self.level = level
        self.id = id
        self.name = name
        self.items = items if items is not None else []
        self.parent = parent
        self._value: Decimal | None = Decimal(value) if value is not None else None

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
        result = _fetch_value_backward(self, None)
        return result if result is not None else Decimal(0)


def _is_decimal(x: Decimal | None) -> typing.TypeGuard[Decimal]:
    return x is not None


def _fetch_value_forward(
    item: DesireItem, ignore: DesireItem | None = None
) -> Decimal | None:
    if item._value is not None:
        return item._value

    sub_items_v: filter[Decimal] = filter(
        _is_decimal,
        [_fetch_value_forward(i) for i in item.items if i != ignore],
    )
    return max(sub_items_v, default=None)


def _fetch_value_backward(
    item: DesireItem, origin: DesireItem | None
) -> Decimal | None:
    item_and_child_v: Decimal | None = _fetch_value_forward(item, origin)

    if item_and_child_v is not None:
        return item_and_child_v

    parent_v = (
        _fetch_value_backward(item.parent, item) if item.parent is not None else None
    )
    return parent_v


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


def _get_desire_item_placeholder_by_name(name: str) -> DesireItem:
    return DesireItem("UNDEFINED", f"未知欲望【{name}】", "XX", 5)


DESIRE_ROOT_PROPERTY: DesireItem = _data_to_desire_tree(load_data("desire"))

DESIRE_ID_TO_NAME: dict[str, str] = load_data("desire_name")


class Desire:
    DESIRE_COUNT = 29

    def __init__(self) -> None:
        self.root = copy.deepcopy(DESIRE_ROOT_PROPERTY)
        self._node_layers: list[dict[str, DesireItem]] = []
        self._build_node_layers()
        self._all_nodes: set[DesireItem] = set()
        self._id2nodes: dict[str, DesireItem] = {}
        self._name2nodes: dict[str, DesireItem] = {}
        self._build_node_dict()

        try:
            self.validate_all_nodes()
        except ValueError as e:
            raise e

    def _build_node_layers(self):
        self._node_layers = [{self.root.id: self.root}]
        layer: dict[str, DesireItem] = dict([(i.id, i) for i in self.root.items])

        while len(layer) > 0:
            self._node_layers.append(layer)
            layer = dict(
                [(i.id, i) for n in self._node_layers[-1].values() for i in n.items]
            )

    def _build_node_dict(self):
        self._id2nodes = {}
        self._name2nodes = {}

        for layer in self._node_layers:
            for node in layer.values():
                self._all_nodes.add(node)
                assert (
                    node.id not in self._id2nodes
                ), f"node.id {node.id} already in self._id2nodes."
                self._id2nodes[node.id] = node
                assert (
                    node.id not in self._name2nodes
                ), f"node.name {node.name} already in self._name2nodes."
                self._name2nodes[node.name] = node

    def validate_all_nodes(self) -> None:
        id_set = set()
        duplicate_ids = set()
        for node in self._all_nodes:
            if node.id in id_set:
                duplicate_ids.add(node.id)
            id_set.add(node.id)
        if duplicate_ids:
            raise ValueError(duplicate_ids)

    def get_item_by_name(self, name: str) -> DesireItem:
        if name not in self._name2nodes:
            logger.warning(f"name {name} not in desire nodes")
            return _get_desire_item_placeholder_by_name(name)
        return self._name2nodes[name]

    @property
    def first_layer(self):
        ids = ["DN", "DS", "DD"]
        return [0] + [self._id2nodes[i].value for i in ids]

    @property
    def second_layer(self):
        base = [("DN", 4), ("DS", 5), ("DD", 4)]
        node_ids = [
            f"{prefix}{i}" for prefix, count in base for i in range(1, count + 1)
        ]
        return [0] + [self._id2nodes[i].value for i in node_ids]

    @property
    def third_layer(self):
        return [0] + [
            self._id2nodes[f"D{i}"].value for i in range(1, Desire.DESIRE_COUNT + 1)
        ]

    @third_layer.setter
    def third_layer(self, value: list):
        for i, v in enumerate(value):
            self._id2nodes[f"D{i+1}"]._value = Decimal(v)

    def __setitem__(self, key: int, value: Decimal | int | float):
        assert key > 0 and key <= Desire.DESIRE_COUNT
        dec_value = Decimal(value)
        self._id2nodes[f"D{key}"]._value = dec_value

    def __repr__(self) -> str:
        third_layer_node = [
            self._id2nodes.get(f"D{i}", None) for i in range(1, Desire.DESIRE_COUNT + 1)
        ]
        valid_nodes = dict(
            [(i.name, int(i.value)) for i in third_layer_node if i and i.value > 0]
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

DESIRE_PROPERTY: Desire = Desire()

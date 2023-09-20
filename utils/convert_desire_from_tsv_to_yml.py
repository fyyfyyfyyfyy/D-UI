import os
import typing
from typing import Dict

import yaml


class DesireItem:
    def __init__(
        self,
        code: str,
        id: str,
        name: str,
        init_v: int | None = None,
        items: list["DesireItem"] = None,
    ) -> None:
        self.code = code
        self.id = id
        self.name = name
        self.items = items if items is not None else []
        self.init_v = init_v

    def to_dict(self) -> dict:
        target: dict[str, typing.Any] = {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "init_v": self.init_v,
        }
        if len(self.items) > 0:
            target["items"] = [item.to_dict() for item in self.items]

        return target


def process_data(data) -> DesireItem:
    lines = data.strip().split("\n")
    root = DesireItem("RL0", "DROOT", "ROOT")
    stack: list[DesireItem] = [root]

    d_code = ""
    d_id = ""
    d_name = ""
    id_count: Dict[str, int] = {}  # Dictionary to track ID

    for line in lines:
        parts = line.split("\t")
        assert len(parts) == 4

        p_code, id, name, init_v = parts

        if len(p_code) > 0:
            assert len(p_code) == 3
            assert p_code[1] == "L", "desire code must contain L meaning code"
            assert p_code[2:].isdigit(), "desire code must end with L"

            d_code = p_code

        d_id, d_name = id, name
        d_init_v = int(init_v)

        item = DesireItem(d_code, d_id, d_name, d_init_v)

        level = int(d_code[2:])

        if level > len(stack):
            assert level - len(stack) == 1, "desire code should increase by 1"

        while level < len(stack):
            parent = stack[-2]
            child = stack.pop()
            parent.items.append(child)

        if d_code[0] == "D" and d_code == p_code:
            print(p_code, item.to_dict(), len(stack))

        stack.append(item)

    while len(stack) > 1:
        parent = stack[-2]
        child = stack.pop()
        parent.items.append(child)

    # Output duplicate IDs and their counts
    duplicate_ids = [id for id, count in id_count.items() if count > 1]
    if duplicate_ids:
        print("Duplicate IDs:")
        for id in duplicate_ids:
            print(f"ID: {id}, Count: {id_count[id]}")

    return stack[0]


def generate_yaml(data):
    yaml_data = yaml.dump(
        data, default_flow_style=False, allow_unicode=True, sort_keys=False
    )
    return yaml_data


def generate_zh_yaml(data):
    yaml_data = {}

    def recursive_parse(item):
        yaml_data[item["id"]] = [{"zh": item["name"]}]

        if "items" in item:
            for sub_item in item["items"]:
                recursive_parse(sub_item)

    for item in data:
        recursive_parse(item)

    return yaml_data


def merge_yamls(yaml1, yaml2):
    merged = {**yaml1, **yaml2}

    for k, v in merged.items():
        if isinstance(v, list):
            v1 = yaml1.get(k)
            v2 = yaml2.get(k)
        if v1 and v2:
            merged[k] = sorted(
                [dict(t) for t in {tuple(d.items()) for d in v1 + v2}],
                key=lambda x: list(x.keys())[0],
            )

    return merged


if __name__ == "__main__":
    with open("desire.tsv", "r", encoding="utf-8") as f:
        raw_data = f.read()

    desire_root = process_data(raw_data)
    yaml_output = generate_yaml(desire_root.to_dict())
    # print(yaml_output)

    with open("desire_out.yml", "w") as f:
        yaml.dump(
            desire_root.to_dict()["items"],
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )

    yaml_zh = generate_zh_yaml(desire_root.to_dict()["items"])

    if os.path.exists("desire_name.yml"):
        with open("desire_name.yml") as f:
            yaml1 = yaml.load(f, Loader=yaml.FullLoader)
        res = merge_yamls(yaml1, yaml_zh)
        with open("desire_name.yml", "w") as f:
            yaml.dump(
                res,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )
    else:
        with open("desire_name.yml", "w") as f:
            yaml.dump(
                yaml_zh,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

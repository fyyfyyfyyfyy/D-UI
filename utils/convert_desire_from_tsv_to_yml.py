import typing

import yaml


class DesireItem:
    def __init__(
        self, code: str, id: str, name: str, items: list["DesireItem"] = None
    ) -> None:
        self.code = code
        self.id = id
        self.name = name
        self.items = items if items is not None else []

    def to_dict(self) -> dict:
        target: dict[str, typing.Any] = {
            "id": self.id,
            "name": self.name,
            "code": self.code,
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

    for line in lines:
        parts = line.split("\t")
        assert len(parts) == 3

        p_code, id, name = parts

        if len(p_code) > 0:
            assert len(p_code) == 3
            assert p_code[1] == "L", "desire code must contain L meaning code"
            assert p_code[2:].isdigit(), "desire code must end with L"

            d_code = p_code

        d_id, d_name = id, name

        item = DesireItem(d_code, d_id, d_name)

        level = int(d_code[2:])

        if level > len(stack):
            assert level - len(stack) == 1, "desire code should increase by 1"

        while level < len(stack):
            parent = stack[-2]
            child = stack.pop()
            parent.items.append(child)

        if d_code[0] == 'D' and d_code == p_code:
            print(p_code, item.to_dict(), len(stack))

        stack.append(item)

    while len(stack) > 1:
        parent = stack[-2]
        child = stack.pop()
        parent.items.append(child)

    return stack[0]


def generate_yaml(data):
    yaml_data = yaml.dump(
        data, default_flow_style=False, allow_unicode=True, sort_keys=False
    )
    return yaml_data


if __name__ == "__main__":
    with open("desire.tsv", "r") as f:
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

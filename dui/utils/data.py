import os
import typing

import yaml

DATA_BASE = "data"


def key2filepath(key: str) -> str:
    return os.path.join(DATA_BASE, f"{key}.yml")


def load_data(key: str) -> typing.Any:
    try:
        filepath = key2filepath(key)
        with open(filepath, "r", encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return None


def save_config(key: str, data: typing.Any):
    filepath = key2filepath(key)
    with open(filepath, "w", encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True)

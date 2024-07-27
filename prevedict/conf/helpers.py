import json
from copy import deepcopy
from pathlib import Path


def merge_dicts(dict1: dict[str], dict2: dict[str]) -> dict[str]:
    """
    Recursively merge two dictionaries, returning a new dict with leaf values on
    dict1 updated with values of dict2.
    """
    new_dict = deepcopy(dict1)

    def recurse(dict1: dict[str], dict2: dict[str]) -> dict[str]:
        for key, value in dict2.items():
            are_dicts = isinstance(dict1[key], dict) and isinstance(value, dict)
            if key in dict1 and are_dicts:
                dict1[key] = merge_dicts(dict1[key], value)
            else:
                # Otherwise, simply update the value
                dict1[key] = value
        return dict1

    return recurse(new_dict, dict2)


def load_from_json(path: Path) -> dict[str]:
    if not path.exists():
        return {}

    with path.open(encoding="utf-8") as f:
        return json.load(f)


def dump_to_json(data: dict[str], path: Path) -> None:
    with path.open("w") as f:
        return json.dump(data, f)


def get_updated_subset_keys(full_dict: dict[str], subset_dict: dict[str]) -> dict[str]:
    """
    Recursively compare two dictionaries, and extract only the keys that have been
    updated with non-default values.
    """

    def recursive_keys(f_dict: dict[str], s_dict: dict[str]) -> dict[str]:
        new = {}
        for key, value in s_dict.items():
            if key in f_dict:
                if isinstance(value, dict) and isinstance(f_dict[key], dict):
                    nested_keys = recursive_keys(f_dict[key], value)
                    if any(nested_keys.values()):
                        new[key] = nested_keys
                else:
                    if f_dict[key] == value:
                        continue
                    new[key] = f_dict[key] != value
        return new

    return recursive_keys(full_dict, subset_dict)


def from_keys_recursive(d: dict[str]) -> dict[str]:
    new_d = dict.fromkeys(d.keys())

    for k, v in d.items():
        if isinstance(v, dict):
            new_d[k] = from_keys_recursive(v)

    return new_d

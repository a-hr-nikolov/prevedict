from typing import ClassVar

from pydantic import BaseModel

from prevedict.conf import defaults, helpers, paths


def dimensions() -> list[int]:
    return list(defaults.WINCONFIG["main_window"]["geometry"])


class MainWindow(BaseModel):
    maximized: bool
    geometry: list[int]


class Splitter(BaseModel):
    proportions: list[int]


class WinConfig(BaseModel):
    main_window: MainWindow
    splitter: Splitter
    _instance: ClassVar["WinConfig"] = None

    def save(self) -> None:
        current = self.model_dump()
        to_dump = helpers.get_updated_subset_keys(defaults.WINCONFIG, current)
        if not to_dump:
            helpers.dump_to_json({}, paths.WINCONFIG)

        dumped = self.model_dump(include=to_dump)
        helpers.dump_to_json(dumped, paths.WINCONFIG)

    @classmethod
    def __load(cls) -> "WinConfig":
        from_json = helpers.load_from_json(paths.WINCONFIG)
        merged = helpers.merge_dicts(defaults.WINCONFIG, from_json)

        return cls(**merged)

    @classmethod
    def instance(cls) -> "WinConfig":
        if cls._instance:
            return cls._instance

        cls._instance = cls.__load()
        return cls._instance

    @classmethod
    def restore_defaults(cls) -> None:
        helpers.dump_to_json({}, paths.WINCONFIG)
        cls._instance = cls.__load()

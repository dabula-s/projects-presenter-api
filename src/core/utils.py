from dataclasses import asdict
from datetime import date
from datetime import datetime
from typing import Any
from typing import Iterable

from dacite import Config
from dacite import from_dict

from core.dto import UNSET


def asdict_extended(obj: Any, exclude_fields: list[str] | None = None):
    if exclude_fields is None:
        exclude_fields = []
    else:
        exclude_fields = set(exclude_fields)

    def dict_factory_with_exclude_option(data: Iterable[tuple[Any, Any]]) -> dict[str, Any]:
        return dict((key, value) for key, value in data if value != UNSET and key not in exclude_fields)

    return asdict(obj, dict_factory=dict_factory_with_exclude_option)


def from_dict_extended(dataclass, data):
    config = Config(
        type_hooks={
            datetime: datetime.fromisoformat,
            date: date.fromisoformat,
        },
    )
    return from_dict(dataclass, data, config)

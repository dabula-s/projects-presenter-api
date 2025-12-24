from __future__ import annotations


from dataclasses import dataclass
from dataclasses import field
from datetime import datetime

from core.exceptions import InvalidTechnologyVersionFormat
from core.exceptions import ProjectDuplicateTechnologyError
from core.exceptions import ProjectInvalidDateRangeError


@dataclass
class Technology:
    name: str
    id: int | None = None
    description: str | None = None


@dataclass
class TechnologyVersion:
    technology: Technology
    version: str
    id: int | None = None

    def validate(self): ...
        #TODO: implement version validation (errors with Snowflake Enterprise, etc.)

        # from packaging.version import InvalidVersion
        # from packaging.version import parse
        # try:
        #     return parse(self.version)
        # except InvalidVersion:
        #     raise InvalidTechnologyVersionFormat(self.technology.name, self.version)

    def __post_init__(self):
        self.validate()

@dataclass
class Project:
    name: str
    id: int | None = None
    description: str | None = None
    technologies: list[TechnologyVersion] = field(default_factory=list)
    start_date: datetime | None = None
    end_date: datetime | None = None

    def validate(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ProjectInvalidDateRangeError(self.start_date, self.end_date)

        tech_list = [tech_version.technology.name for tech_version in self.technologies]
        if len(set(tech_list)) != len(tech_list):
            raise ProjectDuplicateTechnologyError()

    def __post_init__(self):
        self.validate()


from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class UNSET:

    def __repr__(self) -> str:
        return "UNSET"


@dataclass(frozen=True)
class ProjectTechnologyVersionDTO:
    name: str
    version: str


@dataclass(frozen=True)
class GetProjectDTO:
    project_id: int


@dataclass(frozen=True)
class GetProjectsDTO:
    limit: int = 10
    offset: int = 0


@dataclass(frozen=True)
class CreateProjectDTO:
    name: str
    description: str | None | UNSET = UNSET
    technologies: list[ProjectTechnologyVersionDTO] | None | UNSET = UNSET
    start_date: datetime | None | UNSET = UNSET
    end_date: datetime | None | UNSET = UNSET


@dataclass(frozen=True)
class UpdateProjectDTO:
    project_id: int
    name: str | None | UNSET = UNSET
    description: str | None | UNSET = UNSET
    technologies: list[ProjectTechnologyVersionDTO] | None | UNSET = UNSET
    start_date: datetime | None | UNSET = UNSET
    end_date: datetime | None | UNSET = UNSET


@dataclass(frozen=True)
class UpdateProjectTechnologiesDTO:
    project_id: int
    technologies: list[ProjectTechnologyVersionDTO]


@dataclass(frozen=True)
class RemoveProjectTechnologiesDTO:
    project_id: int
    technologies: list[str]


@dataclass(frozen=True)
class DeleteProjectDTO:
    project_id: int

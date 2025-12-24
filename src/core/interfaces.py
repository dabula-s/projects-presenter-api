from typing import Iterable
from typing import Protocol

from core.dto import CreateProjectDTO
from core.dto import DeleteProjectDTO
from core.dto import GetProjectDTO
from core.dto import GetProjectsDTO
from core.dto import RemoveProjectTechnologiesDTO
from core.dto import UpdateProjectDTO
from core.dto import UpdateProjectTechnologiesDTO
from core.entities import Project


class ProjectRepository(Protocol):

    def get_many(self, dto: GetProjectsDTO) -> Iterable[Project]: ...

    def get_by_id(self, dto: GetProjectDTO) -> Project: ...

    def create(self, dto: CreateProjectDTO) -> Project: ...

    def update(self, dto: UpdateProjectDTO) -> Project: ...

    def update_technologies(self, dto: UpdateProjectTechnologiesDTO) -> Project: ...

    def remove_technologies(self, dto: RemoveProjectTechnologiesDTO) -> Project: ...

    def delete(self, dto: DeleteProjectDTO) -> bool: ...

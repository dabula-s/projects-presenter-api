from abc import ABC
from typing import Iterable

from core.dto import CreateProjectDTO
from core.dto import DeleteProjectDTO
from core.dto import GetProjectDTO
from core.dto import GetProjectsDTO
from core.dto import RemoveProjectTechnologiesDTO
from core.dto import UpdateProjectDTO
from core.dto import UpdateProjectTechnologiesDTO
from core.entities import Project
from core.interfaces import ProjectRepository


class BaseProjectService(ABC):

    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository


class GetManyProjectsService(BaseProjectService):

    def call(self, dto: GetProjectsDTO) -> Iterable[Project]:
        return self.project_repository.get_many(dto=dto)


class GetSingleProjectService(BaseProjectService):

    def call(self, dto: GetProjectDTO) -> Project:
        return self.project_repository.get_by_id(dto=dto)


class CreateProjectService(BaseProjectService):

    def call(self, dto: CreateProjectDTO) -> Project:
        return self.project_repository.create(dto=dto)


class UpdateProjectService(BaseProjectService):

    def call(self, dto: UpdateProjectDTO) -> Project:
        return self.project_repository.update(dto=dto)


class UpdateProjectTechnologiesService(BaseProjectService):

    def call(self, dto: UpdateProjectTechnologiesDTO) -> Project:
        return self.project_repository.update_technologies(dto=dto)


class RemoveProjectTechnologies(BaseProjectService):

    def call(self, dto: RemoveProjectTechnologiesDTO) -> Project:
        return self.project_repository.remove_technologies(dto=dto)


class DeleteProjectService(BaseProjectService):

    def call(self, dto: DeleteProjectDTO) -> bool:
        return self.project_repository.delete(dto=dto)

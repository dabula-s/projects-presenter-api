import logging
from typing import Iterable

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import tuple_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload

from core.dto import CreateProjectDTO
from core.dto import DeleteProjectDTO
from core.dto import GetProjectDTO
from core.dto import GetProjectsDTO
from core.dto import ProjectTechnologyVersionDTO
from core.dto import RemoveProjectTechnologiesDTO
from core.dto import UNSET
from core.dto import UpdateProjectDTO
from core.dto import UpdateProjectTechnologiesDTO
from core.entities import Project
from core.entities import Technology
from core.entities import TechnologyVersion
from core.exceptions import ProjectNameAlreadyExistsError
from core.exceptions import ProjectNotFoundError
from core.utils import asdict_extended
from infrastructure.db.postgres.models import ProjectModel
from infrastructure.db.postgres.models import TechnologyModel
from infrastructure.db.postgres.models import TechnologyVersionModel

logger = logging.getLogger(__name__)

class PostgresProjectRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_many(self, dto: GetProjectsDTO) -> Iterable[Project]:
        projects = self.session.execute(
            select(ProjectModel)
            .options(
                selectinload(ProjectModel.technologies).joinedload(TechnologyVersionModel.technology),
            ).offset(dto.offset).limit(dto.limit),
        ).scalars().all()

        return list(map(self._to_entity, projects))

    def get_by_id(self, dto: GetProjectDTO) -> Project:
        project = self._get_by_id(project_id=dto.project_id)

        return self._to_entity(project)

    def create(self, dto: CreateProjectDTO) -> Project:
        try:
            project = ProjectModel(**asdict_extended(dto, exclude_fields=['technologies']))
            self.session.add(project)

            if dto.technologies and dto.technologies != UNSET:
                technologies = self._get_or_create_tech_versions(technologies=dto.technologies)
                project.technologies = technologies

            self.session.flush()
        except IntegrityError as e:
            if 'project_name_key' in str(e.orig):
                raise ProjectNameAlreadyExistsError(dto.name) from e
            raise

        return self._to_entity(project)

    def update(self, dto: UpdateProjectDTO) -> Project:
        try:
            project = self._get_by_id(project_id=dto.project_id)
            for key, value in asdict_extended(dto, exclude_fields=['project_id', 'technologies']).items():
                setattr(project, key, value)
            if not dto.technologies and dto.technologies is not None:
                project.technologies = []
            elif dto.technologies and dto.technologies != UNSET:
                technologies = self._get_or_create_tech_versions(technologies=dto.technologies)
                project.technologies = technologies

            self.session.flush()
        except IntegrityError as e:
            if 'project_name_key' in str(e.orig):
                raise ProjectNameAlreadyExistsError(dto.name) from e
            raise

        return self._to_entity(project)

    def update_technologies(self, dto: UpdateProjectTechnologiesDTO) -> Project:
        project = self._get_by_id(project_id=dto.project_id)
        if not dto.technologies:
            return self._to_entity(project)

        tech_version_map = {tech_version.technology.name: tech_version.version for tech_version in project.technologies}
        tech_versions_new_map = {tech_version.name: tech_version.version for tech_version in dto.technologies}
        tech_version_map.update(tech_versions_new_map)

        technologies = self._get_or_create_tech_versions(
            [
                ProjectTechnologyVersionDTO(name=name, version=version)
                for name, version
                in tech_version_map.items()
            ],
        )
        project.technologies = technologies

        self.session.flush()

        return self._to_entity(project)

    def remove_technologies(self, dto: RemoveProjectTechnologiesDTO) -> Project:
        project = self._get_by_id(project_id=dto.project_id)
        if not dto.technologies:
            return self._to_entity(project)

        tech_versions_remove_list = [tech_version for tech_version in dto.technologies]
        tech_versions_list = [
            tech_version
            for tech_version
            in project.technologies
            if tech_version.technology.name not in tech_versions_remove_list
        ]
        project.technologies = tech_versions_list
        self.session.flush()

        return self._to_entity(project)

    def delete(self, dto: DeleteProjectDTO) -> bool:
        result = self.session.execute(delete(ProjectModel).where(ProjectModel.id == dto.project_id))
        if result.rowcount:
            return True
        return False

    def _get_by_id(self, project_id: int) -> ProjectModel:
        project = self.session.execute(
            select(ProjectModel)
            .options(selectinload(ProjectModel.technologies).joinedload(TechnologyVersionModel.technology))
            .where(ProjectModel.id == project_id),
        ).scalars().first()

        if project is None:
            raise ProjectNotFoundError(project_id)

        return project

    @staticmethod
    def _to_entity(project: ProjectModel) -> Project:
        return Project(
            id=project.id,
            name=project.name,
            description=project.description,
            technologies=[
                TechnologyVersion(
                    id=t.id,
                    technology=Technology(
                        id=t.technology.id,
                        name=t.technology.name,
                        description=t.technology.description,
                    ),
                    version=t.version,
                )
                for t
                in project.technologies
            ],
            start_date=project.start_date,
            end_date=project.end_date,
        )

    def _get_or_create_tech_versions(self, technologies: list[ProjectTechnologyVersionDTO]) -> list[
        TechnologyVersionModel]:
        self.session.execute(
            insert(TechnologyModel)
            .values([{'name': tech.name} for tech in technologies])
            .on_conflict_do_nothing(index_elements=['name']),
        )
        existing_techs = self.session.execute(
            select(TechnologyModel)
            .where(TechnologyModel.name.in_([tech.name for tech in technologies])),
        ).scalars().all()

        existing_techs_map = {tech.name: tech for tech in existing_techs}

        tech_versions_insert_values = [
            {'version': tech.version, 'technology_id': existing_techs_map[tech.name].id}
            for tech
            in technologies
        ]
        self.session.execute(
            insert(TechnologyVersionModel)
            .values(tech_versions_insert_values)
            .on_conflict_do_nothing(index_elements=['technology_id', 'version']),
        )

        tech_versions_pairs = [(existing_techs_map[tech.name].id, tech.version) for tech in technologies]
        tech_versions = self.session.execute(
            select(TechnologyVersionModel)
            .where(
                tuple_(TechnologyVersionModel.technology_id, TechnologyVersionModel.version)
                .in_(tech_versions_pairs),
            )
            .options(joinedload(TechnologyVersionModel.technology)),
        ).scalars().all()

        return list(tech_versions)

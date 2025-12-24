from flask import Blueprint
from flask import jsonify

from application.services import CreateProjectService
from application.services import DeleteProjectService
from application.services import GetManyProjectsService
from application.services import GetSingleProjectService
from application.services import RemoveProjectTechnologies
from application.services import UpdateProjectService
from application.services import UpdateProjectTechnologiesService
from core.dto import CreateProjectDTO
from core.dto import DeleteProjectDTO
from core.dto import GetProjectDTO
from core.dto import GetProjectsDTO
from core.dto import RemoveProjectTechnologiesDTO
from core.dto import UpdateProjectDTO
from core.dto import UpdateProjectTechnologiesDTO
from core.utils import from_dict_extended
from infrastructure.db.postgres import PostgresProjectRepository
from infrastructure.db.postgres import sync_session_manager
from presentation.api.schemas import CreateProjectRequestSchema
from presentation.api.schemas import CreateProjectResponseSchema
from presentation.api.schemas import DeleteProjectRequestSchema
from presentation.api.schemas import DeleteProjectResponseSchema
from presentation.api.schemas import GetManyProjectRequestSchema
from presentation.api.schemas import GetManyProjectResponseSchema
from presentation.api.schemas import GetProjectResponseSchema
from presentation.api.schemas import ProjectSchema
from presentation.api.schemas import RemoveProjectTechnologiesJsonSchema
from presentation.api.schemas import UpdateProjectJsonSchema
from presentation.api.schemas import UpdateProjectResponseSchema
from presentation.api.schemas import UpdateProjectTechnologiesJsonSchema
from presentation.api.swagger import spec

projects_router = Blueprint('projects', __name__, url_prefix='/project')


@projects_router.route('/<int:project_id>', methods=['GET'])
@spec.validate(
    tags=['Projects'],
)
def get_project(project_id: int):
    with sync_session_manager() as session:
        project_repository = PostgresProjectRepository(session=session)
        service = GetSingleProjectService(project_repository=project_repository)
        service_dto = from_dict_extended(GetProjectDTO, {'project_id': project_id})
        project = service.call(dto=service_dto)

    return jsonify(GetProjectResponseSchema.model_validate(project).model_dump(mode='json')), 200


@projects_router.route('/all', methods=['GET'])
@spec.validate(
    query=GetManyProjectRequestSchema,
    tags=['Projects'],
)
def get_projects(query: GetManyProjectRequestSchema):
    with sync_session_manager() as session:
        project_repository = PostgresProjectRepository(session=session)
        service = GetManyProjectsService(project_repository=project_repository)
        service_dto = from_dict_extended(GetProjectsDTO, query.model_dump(exclude_unset=True))
        projects = service.call(dto=service_dto)

    result_projects = []
    for project in projects:
        result_projects.append(ProjectSchema.model_validate(project))

    return jsonify(GetManyProjectResponseSchema(
        projects=result_projects,
        next_offset=query.offset + query.limit,
    ).model_dump(mode='json')), 200


@projects_router.route('/', methods=['POST'])
@spec.validate(
    json=CreateProjectRequestSchema,
    tags=['Projects'],
)
def create_project(json: CreateProjectRequestSchema):
    with sync_session_manager() as session:
        project_repository = PostgresProjectRepository(session=session)
        service = CreateProjectService(project_repository=project_repository)
        service_dto = from_dict_extended(CreateProjectDTO, json.model_dump(mode='json', exclude_unset=True))
        project = service.call(dto=service_dto)

    return jsonify(CreateProjectResponseSchema.model_validate(project).model_dump(mode='json')), 201


@projects_router.route('/<int:project_id>', methods=['PATCH'])
@spec.validate(
    json=UpdateProjectJsonSchema,
    tags=['Projects'],
)
def update_project(project_id: int, json: UpdateProjectJsonSchema):
    with sync_session_manager() as session:
        project_repository = PostgresProjectRepository(session=session)
        service = UpdateProjectService(project_repository=project_repository)
        service_dto = from_dict_extended(UpdateProjectDTO,
                                         {'project_id': project_id,
                                          **json.model_dump(mode='json', exclude_unset=True)})
        project = service.call(dto=service_dto)

    return jsonify(UpdateProjectResponseSchema.model_validate(project).model_dump(mode='json')), 200


@projects_router.route('/<int:project_id>/technologies/update', methods=['POST'])
@spec.validate(
    json=UpdateProjectTechnologiesJsonSchema,
    tags=['Projects'],
)
def update_project_technologies(project_id: int, json: UpdateProjectTechnologiesJsonSchema):
    with sync_session_manager() as session:
        project_repository = PostgresProjectRepository(session=session)
        service = UpdateProjectTechnologiesService(project_repository=project_repository)
        service_dto = from_dict_extended(UpdateProjectTechnologiesDTO,
                                         {'project_id': project_id, **json.model_dump(mode='json', exclude_unset=True)})
        project = service.call(dto=service_dto)

    return jsonify(UpdateProjectResponseSchema.model_validate(project).model_dump(mode='json')), 200


@projects_router.route('/<int:project_id>/technologies/remove', methods=['POST'])
@spec.validate(
    json=RemoveProjectTechnologiesJsonSchema,
    tags=['Projects'],
)
def remove_project_technologies(project_id: int, json: RemoveProjectTechnologiesJsonSchema):
    with sync_session_manager() as session:
        project_repository = PostgresProjectRepository(session=session)
        service = RemoveProjectTechnologies(project_repository=project_repository)
        service_dto = from_dict_extended(RemoveProjectTechnologiesDTO,
                                         {'project_id': project_id, **json.model_dump(mode='json', exclude_unset=True)})
        project = service.call(dto=service_dto)

    return jsonify(UpdateProjectResponseSchema.model_validate(project).model_dump(mode='json')), 200


@projects_router.route('/<int:project_id>', methods=['DELETE'])
@spec.validate(
    tags=['Projects'],
)
def delete_project(project_id: int):
    request_dto = DeleteProjectRequestSchema(project_id=project_id)
    with sync_session_manager() as session:
        project_repository = PostgresProjectRepository(session=session)
        service = DeleteProjectService(project_repository=project_repository)
        service_dto = from_dict_extended(DeleteProjectDTO, request_dto.model_dump(exclude_unset=True))
        success = service.call(dto=service_dto)

    return jsonify(DeleteProjectResponseSchema(success=success).model_dump(mode='json')), 200

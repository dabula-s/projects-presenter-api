from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
from pydantic import model_validator


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra='forbid',
        str_strip_whitespace=True,
        from_attributes=True,
    )


class AtLeastOneFieldRequiredMixin(BaseModel):

    @model_validator(mode='after')
    def check_at_least_one_field(self):
        submitted_data = self.model_dump(exclude_unset=True)

        if not submitted_data:
            raise ValueError('At least one field must be provided!')

        return self


# TODO: create custom type for version

class TechnologySchema(BaseSchema):
    id: int | None = None
    name: str = Field(..., min_length=1, max_length=128, examples=['Flask', 'Python'])
    description: str | None = Field(None, min_length=1, max_length=255)


class TechnologyVersionSchema(BaseSchema):
    id: int | None = None
    version: str = Field(..., min_length=1, max_length=128, examples=['Enterprise', '3.12', '12.233.1'])
    technology: TechnologySchema


class ProjectSchema(BaseSchema):
    id: int | None = None
    name: str = Field(..., min_length=1, max_length=128)
    description: str | None = Field(None, min_length=1, max_length=255)
    technologies: set[TechnologyVersionSchema] = Field(default_factory=set)
    start_date: datetime | None = None
    end_date: datetime | None = None


class ProjectTechnologyVersionSchema(BaseSchema):
    name: str = Field(..., min_length=1, max_length=128)
    version: str


class ProjectIdPathParameterSchema(BaseSchema):
    project_id: int = Field(..., ge=0)


class GetProjectResponseSchema(ProjectSchema):
    ...


class GetManyProjectRequestSchema(BaseSchema):
    limit: int = Field(10, gt=0)
    offset: int = Field(0, ge=0)


class GetManyProjectResponseSchema(BaseSchema):
    projects: list[ProjectSchema]
    next_offset: int = Field(0, ge=0)


class CreateProjectRequestSchema(BaseSchema):
    name: str = Field(..., min_length=1, max_length=128, examples=['Project name'])
    description: str | None = Field(None, min_length=1, max_length=255, examples=['Some description'])
    technologies: set[ProjectTechnologyVersionSchema] | None = Field(None, examples=[
        [
            {"name": "Python", "version": "3.12"},
            {"name": "Flask", "version": "3.0.0"},
            {"name": "PostgreSQL", "version": "16.1"},
        ],
    ])
    start_date: datetime | None = Field(None, examples=['2025-01-01T00:00:00'])
    end_date: datetime | None = Field(None, examples=['2025-12-31T00:00:00'])


class CreateProjectResponseSchema(ProjectSchema):
    ...


class UpdateProjectJsonSchema(BaseSchema, AtLeastOneFieldRequiredMixin):
    name: str = Field(..., min_length=1, max_length=128, examples=['Project new name'])
    description: str | None = Field(None, min_length=1, max_length=255, examples=['Some new description'])
    technologies: set[ProjectTechnologyVersionSchema] | None = Field(None, examples=[
        [
            {"name": "Python", "version": "3.12"},
            {"name": "Flask", "version": "3.0.0"},
            {"name": "PostgreSQL", "version": "16.1"},
        ],
    ])
    start_date: datetime | None = Field(None, examples=['2025-01-01T00:00:00'])
    end_date: datetime | None = Field(None, examples=['2025-12-31T00:00:00'])

    @field_validator('name')
    @classmethod
    def validate_not_none(cls, value: str):
        if value is None:
            raise ValueError('Name cannot be empty!')

        return value


class UpdateProjectResponseSchema(ProjectSchema):
    ...


class UpdateProjectTechnologiesJsonSchema(BaseSchema):
    technologies: set[ProjectTechnologyVersionSchema]


class UpdateProjectTechnologiesResponseSchema(ProjectSchema):
    ...


class RemoveProjectTechnologiesJsonSchema(BaseSchema):
    technologies: set[str]


class RemoveProjectTechnologiesRequestSchema(BaseSchema):
    project_id: int
    technologies: set[str]


class RemoveProjectTechnologiesResponseSchema(ProjectSchema):
    ...


class DeleteProjectRequestSchema(BaseSchema):
    project_id: int


class DeleteProjectResponseSchema(BaseSchema):
    success: bool

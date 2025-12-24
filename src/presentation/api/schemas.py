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
    name: str = Field(..., min_length=1, max_length=128)
    description: str | None = Field(None, min_length=1, max_length=255)


class TechnologyVersionSchema(BaseSchema):
    id: int | None = None
    version: str = Field(..., min_length=1, max_length=128)
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
    name: str = Field(..., min_length=1, max_length=128)
    description: str | None = Field(None, min_length=1, max_length=255)
    technologies: set[ProjectTechnologyVersionSchema] | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None


class CreateProjectResponseSchema(ProjectSchema):
    ...


class UpdateProjectJsonSchema(BaseSchema, AtLeastOneFieldRequiredMixin):
    name: str | None = Field(None, min_length=1, max_length=128)
    description: str | None = Field(None, min_length=1, max_length=255)
    technologies: set[ProjectTechnologyVersionSchema] | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None

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

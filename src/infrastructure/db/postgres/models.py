from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from infrastructure.db.postgres.base import BaseModel


class TechnologyModel(BaseModel):
    __tablename__ = 'technology'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str | None] = mapped_column(String(255))

    versions: Mapped[list["TechnologyVersionModel"]] = relationship(back_populates="technology")

    __table_args__ = (UniqueConstraint('name'),)


class TechnologyVersionModel(BaseModel):
    __tablename__ = 'technology_version'

    id: Mapped[int] = mapped_column(primary_key=True)
    technology_id: Mapped[int] = mapped_column(ForeignKey('technology.id'))
    technology: Mapped[TechnologyModel] = relationship(back_populates='versions')
    version: Mapped[str] = mapped_column(String(128))

    __table_args__ = (UniqueConstraint('technology_id', 'version'),)


class ProjectTechnologyAssociationModel(BaseModel):
    __tablename__ = 'project_technology_association'
    project_id: Mapped[int] = mapped_column(ForeignKey('project.id'), primary_key=True)
    technology_version_id: Mapped[int] = mapped_column(ForeignKey('technology_version.id'), primary_key=True)


class ProjectModel(BaseModel):
    __tablename__ = 'project'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    start_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    technologies: Mapped[list[TechnologyVersionModel]] = relationship(
        secondary=ProjectTechnologyAssociationModel.__table__,
    )

    __table_args__ = (UniqueConstraint('name'),)

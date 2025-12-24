import json
import logging

import click

from application.services import CreateProjectService
from core.dto import CreateProjectDTO
from core.exceptions import ProjectNameAlreadyExistsError
from core.utils import from_dict_extended
from infrastructure.db.postgres import PostgresProjectRepository
from infrastructure.db.postgres import sync_session_manager

logger = logging.getLogger(__name__)


@click.group()
def database():
    pass


@database.command()
@click.argument('path', default='seed/projects.json', type=click.Path(exists=True))
def seed(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            projects_data = json.load(file)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.error(f"Failed to decode JSON file: {e}")
        return

    logger.info(f"Starting seeding from {path}...")

    for project_dict in projects_data:
        try:
            with sync_session_manager() as session:
                repo = PostgresProjectRepository(session)
                service = CreateProjectService(repo)
                dto = from_dict_extended(CreateProjectDTO, project_dict)
                service.call(dto)
                logger.warning(f"Project '{dto.name}' created successfully.")

        except ProjectNameAlreadyExistsError:
            logger.warning(f"Project '{project_dict.get('name')}' already exists. Skipped.")
        except Exception as e:
            logger.error(f"Failed to create project '{project_dict.get('name', 'Unknown')}': {e}")

    logger.info("Seeding process completed.")
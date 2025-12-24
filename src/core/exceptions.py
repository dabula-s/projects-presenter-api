from datetime import datetime


class CoreException(Exception):
    ...


class ProjectNotFoundError(CoreException):

    def __init__(self, project_id: int):
        super().__init__(f'Project with id ({project_id}) not found.')


class ProjectNameAlreadyExistsError(CoreException):

    def __init__(self, name: str):
        super().__init__(f'Project with name ({name}) already exists.')


class ProjectDuplicateTechnologyError(CoreException):

    def __init__(self):
        super().__init__(f'Project technologies must be unique.')


class ProjectInvalidDateRangeError(CoreException):

    def __init__(self, start_date: datetime, end_date: datetime):
        super().__init__(f'Invalid date range: start_date ({start_date}) cannot be after end_date ({end_date}).')

class InvalidTechnologyVersionFormat(CoreException):
    def __init__(self, name:str, version: str):
        super().__init__(f'Technology with name ({name}) has invalid version ({version})')

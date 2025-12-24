from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from settings import POSTGRES_DB
from settings import POSTGRES_HOST
from settings import POSTGRES_PASSWORD
from settings import POSTGRES_PORT
from settings import POSTGRES_USER

sync_connection_url = ('postgresql://'
                       f'{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
                       f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')
sync_engine = create_engine(sync_connection_url)


class BaseModel(DeclarativeBase):
    ...


metadata = BaseModel.metadata

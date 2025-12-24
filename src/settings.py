import os

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

# PostgresSQL
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'projects')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

FLASK_SECRET = os.getenv('FLASK_SECRET')

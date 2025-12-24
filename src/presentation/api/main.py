from flask import Flask

from presentation.api.endpoints import projects_router
from presentation.api.exception_handlers import register_exception_handlers
from presentation.api.swagger import spec
from log import setup_logging


def create_app() -> Flask:
    setup_logging()

    app = Flask(__name__)
    app.register_blueprint(projects_router)
    register_exception_handlers(app)
    spec.register(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()

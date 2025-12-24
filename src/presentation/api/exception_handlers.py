import logging

from flask import Flask
from flask import jsonify
from werkzeug.exceptions import HTTPException

from core.exceptions import CoreException
from core.exceptions import InvalidTechnologyVersionFormat
from core.exceptions import ProjectDuplicateTechnologyError
from core.exceptions import ProjectInvalidDateRangeError
from core.exceptions import ProjectNameAlreadyExistsError
from core.exceptions import ProjectNotFoundError

logger = logging.getLogger(__name__)

EXCEPTION_STATUS_CODES = {
    ProjectNotFoundError: 404,
    ProjectNameAlreadyExistsError: 409,
    ProjectDuplicateTechnologyError: 418,  # haha, find me
    ProjectInvalidDateRangeError: 422,
    InvalidTechnologyVersionFormat: 400,
    CoreException: 500,
}


def register_exception_handlers(app: Flask):
    def create_error_handler(status):
        def handler(error):
            logger.exception('CoreException occurred')
            response = {
                'error': error.__class__.__name__,
                'detail': str(error),
            }
            return jsonify(response), status

        return handler

    for exc_class, status_code in EXCEPTION_STATUS_CODES.items():
        app.register_error_handler(exc_class, create_error_handler(status_code))

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        if isinstance(error, HTTPException):
            return jsonify({
                'error': error.name,
                'detail': error.description
            }), error.code

        logger.exception('Unhandled exception occurred')

        response = {
            'error': 'InternalServerError',
            'detail': 'An unexpected error occurred. Please contact support.'
        }
        return jsonify(response), 500

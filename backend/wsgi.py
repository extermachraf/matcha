import os
from app import create_app, get_db_uri
from app.services.input_validatore import inputValidationExeption


# The app object should only be created inside the main guard when running
# this script directly. This prevents import-time side-effects when the
# module is used by a WSGI server.
if __name__ == '__main__':
    app = create_app()
    print(app.blueprints)    # shows which blueprints are registered
    print(app.url_map)
    @app.errorhandler(inputValidationExeption)
    def handle_validation_error(error):
        """Global handler for validation exceptions."""
        response = jsonify({
            "error": error.args[0], 
            "details": error.errors
        })
        response.status_code = error.status_code
        return response
    # Start the Flask development server
    app.run()
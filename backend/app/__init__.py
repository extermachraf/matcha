from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

import click

# Initialize extensions outside the factory
db = SQLAlchemy()


def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)

    # Load configuration from the specified class
    app.config.from_object(config_class)

    # IMPORTANT: We rely exclusively on `DATABASE_URL` in the environment/.env.
    # `config.Config` should have populated `app.config['DATABASE_URL']`.

    # Initialize extensions with the app
    db.init_app(app)

    # Import and Register Blueprints
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    from app.routes.profile import bp as profile_bp
    app.register_blueprint(profile_bp, url_prefix='/api/profile')

    # Fail-fast DB connectivity check: attempt a minimal query using the
    # same engine Flask-SQLAlchemy will use. If it fails, raise a clear
    # RuntimeError to stop application startup.
    from sqlalchemy import text
    with app.app_context():
        try:
            engine = db.get_engine()
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
        except Exception as e:
            # Provide a clear error that will make container/orchestration
            # systems and local devs aware of the DB problem immediately.
            raise RuntimeError(f"Database connection failed during startup: {e}")

        # If the connectivity check passed, ensure tables exist
        db.create_all()

    # Register a Flask CLI command to test DB connectivity
    @app.cli.command("db-test")
    def db_test():
        """Run a quick DB connectivity test from the Flask CLI.

        Usage: `export FLASK_APP="app:create_app"` then `flask db-test`
        """
        from sqlalchemy import create_engine, text

        db_uri = current_app.config.get('DATABASE_URL')

        click.echo(f"Resolved DB URI: {db_uri or '<none>'}")

        if not db_uri:
            click.echo("❌ No DB URI found. Set DATABASE_URL in .env or export it.")
            raise SystemExit(1)

        try:
            engine = create_engine(db_uri)
            with engine.connect() as conn:
                r = conn.execute(text("SELECT 1"))
                click.echo(f"✅ Connection OK. Test query returned: {r.first()}")
        except Exception as e:
            click.echo(f"❌ Connection failed: {e}")
            raise SystemExit(2)

    return app
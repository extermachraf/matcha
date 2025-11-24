from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from app.repositories.connection import get_db_engine
from app.constants.tags import CATEGORY_IDS, ALL_TAGS
from flask_cors import CORS

import click

# Initialize extensions outside the factory
db = SQLAlchemy()


def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)

    # Load configuration from the specified class
    app.config.from_object(config_class)
    
    print("Config FRONTEND_HOST:", app.config.get('FRONTEND_HOST'))
    CORS(app, 
         resources={r"/api/*": {"origins": "*"}}, # Allow all origins for development
         supports_credentials=True # Crucial for sending cookies (JWT in HTTP-only cookie)
    )

    # IMPORTANT: We rely exclusively on `DATABASE_URL` in the environment/.env.
    # `config.Config` should have populated `app.config['DATABASE_URL']`.

    # Initialize extensions with the app
    db.init_app(app)

    # Import and Register Blueprints
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    from app.routes.profile import bp as profile_bp
    app.register_blueprint(profile_bp, url_prefix='/api/profile')
    
    from app.routes.tags import bp as tags_bp
    app.register_blueprint(tags_bp, url_prefix='/api/tags')

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
        
    @app.cli.command("run-sync-tags")
    def run_sync_tags():
        try:
            engine = get_db_engine()
            with engine.connect() as conn:
                # Example sync operation; replace with actual logic
                conn.execute(text("SELECT 1"))
                click.echo("✅ Tags synchronized successfully.")
        except Exception as e:
            click.echo(f"❌ Tag synchronization failed: {e}")
            raise SystemExit(2)
        category_inserts = []
        categories_to_insert = [
            {'id': category_id, 'name': category_name}
            for category_name, category_id in CATEGORY_IDS.items()
        ]
        
        # --- 2. Generate SQL for Tags ---
        # Create a list of tuples: (name, tag_category_id)
        tags_to_insert = [
            {'name': tag_name, 'tag_category_id': category_id}
            for tag_name, category_id in ALL_TAGS.items()
        ]
        with engine.connect() as connection:
            trans = connection.begin()
        
            try:
                print("Starting Tag Synchronization...")
                
                # **IMPORTANT:** Use TRUNCATE to reset the tables completely 
                # (or DELETE FROM if TRUNCATE is restricted)
                # This ensures old, removed tags don't linger.
                connection.execute(text("TRUNCATE TABLE tag_categories RESTART IDENTITY CASCADE;"))
                print("Cleared existing categories and tags.")

                # Insert Categories (Manual SQL)
                category_sql = "INSERT INTO tag_categories (id, name) VALUES (:id, :name);"
                connection.execute(text(category_sql), categories_to_insert)
                print(f"Inserted {len(categories_to_insert)} categories.")

                # Insert Tags (Manual SQL)
                tag_sql = "INSERT INTO tags (name, tag_category_id) VALUES (:name, :tag_category_id);"
                connection.execute(text(tag_sql), tags_to_insert)
                print(f"Inserted {len(tags_to_insert)} tags.")

                trans.commit()
                print("✅ Tag synchronization complete.")
            
            except Exception as e:
                trans.rollback()
                print(f"❌ Synchronization failed: {e}")
                raise
            
    @app.cli.command("test-email-send")
    def test_email_send():
        """Test sending a verification email using the SMTP handler."""
        from app.services.smtp_handler import send_verification_email
        test_email = "achraf.miam+1@gmail.com"
        test_verification_url = "http://example.com/verify?token=testtoken123"
        if send_verification_email(test_email, test_verification_url):
            print("✅ Test email sent successfully.")        
        else:
            print("❌ Test email failed to send.")
    return app
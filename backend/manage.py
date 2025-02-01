import os
from flask.cli import FlaskGroup
from . import create_app, db  # Import db
from flask_migrate import Migrate

# Get the configuration class from the environment, or default to ProductionConfig
config_class = os.environ.get('FLASK_CONFIG') or 'config.ProductionConfig' # Default to Production
app = create_app(config_class) # Create the Flask app with the chosen config

migrate = Migrate(app, db) # Initialize Migrate *after* app is created


cli = FlaskGroup(create_app=create_app)  # Use FlaskGroup for CLI commands


@cli.command("db")
def db_commands():
    """Perform database operations."""
    pass  # Subcommands for db migrate, upgrade, etc. will be added here


@cli.command("db_create")
def db_create():
    """Creates the database."""
    with app.app_context(): # Important: Use app context
        db.create_all()
    print("Database created.")


@cli.command("db_drop")  # Add a db_drop command
def db_drop():
    """Drops all database tables."""
    with app.app_context(): # Important: Use app context
        db.drop_all()
    print("Database tables dropped.")


@cli.command("db_migrate")
def db_migrate():
    """Migrate the database."""
    migrate.migrate()
    print("Database migrated.")


@cli.command("db_upgrade")
def db_upgrade():
    """Upgrade the database."""
    migrate.upgrade()
    print("Database upgraded.")

@cli.command("db_seed") # Example command to seed data (add as needed)
def db_seed():
    """Seeds the database with initial data."""
    with app.app_context():
        # Example: Add some users
        from .models import User
        if not User.query.filter_by(username='admin').first(): # Check if user exists
            admin_user = User(username='admin', email='admin@example.com', password_hash='pbkdf2:sha256:600000$t9n54vQd$34085751c88309816955d1111423211929a297938d9d89482e736310e149b82f', user_type='client') # Replace with real hashing
            db.session.add(admin_user)
            db.session.commit()
        print("Database seeded.")


if __name__ == "__main__":
    cli()
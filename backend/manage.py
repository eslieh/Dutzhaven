import os
from flask.cli import FlaskGroup
from .app import create_app, db  # Note the explicit path
from flask_migrate import Migrate
from .config import config 

# Determine the configuration class (important!)
config_class = os.environ.get('FLASK_CONFIG') or 'default'  # Use 'default' as string
app = create_app(config[config_class])  # Use config dictionary lookup (important!)

migrate = Migrate(app, db)

cli = FlaskGroup(create_app=create_app)

@cli.command("db")
def db_commands():
    """Perform database operations."""
    pass  # Subcommands for db migrate, upgrade, etc. will be added here

@cli.command("db_create")
def db_create():
    """Creates the database."""
    with app.app_context():
        db.create_all()
    print("Database created.")

@cli.command("db_drop")
def db_drop():
    """Drops all database tables."""
    with app.app_context():
        db.drop_all()
    print("Database tables dropped.")

@cli.command("db_migrate")
def db_migrate():
    """Migrate the database."""
    with app.app_context(): # Add app context here as well
        migrate.migrate()
    print("Database migrated.")

@cli.command("db_upgrade")
def db_upgrade():
    """Upgrade the database."""
    with app.app_context(): # Add app context here as well
        migrate.upgrade()
    print("Database upgraded.")

@cli.command("db_seed")
def db_seed():
    """Seeds the database with initial data."""
    with app.app_context():
        from .models import User
        if not User.query.filter_by(username='admin').first():
            # Hash the password properly (replace with your actual hashing method)
            hashed_password = 'pbkdf2:sha256:600000$t9n54vQd$34085751c88309816955d1111423211929a297938d9d89482e736310e149b82f'  # Replace with real hashing
            admin_user = User(username='admin', email='admin@example.com', password_hash=hashed_password, user_type='client', full_name='Admin User') # Add full_name
            db.session.add(admin_user)
            db.session.commit()
        print("Database seeded.")

if __name__ == "__main__":
    cli()
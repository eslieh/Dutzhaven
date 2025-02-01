from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

# You can add other extensions here as your application grows
# For example:
# from flask_mail import Mail
# mail = Mail()
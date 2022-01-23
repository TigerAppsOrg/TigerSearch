# ----------------------------------------------------------------------
# init.py
# Authors: Anagha Rajagopalan, Mandy Lin, Moin Mir, and Omar El-Kishky
# ----------------------------------------------------------------------

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from tigerapp.config import Config
from flask_login import LoginManager
import cloudinary
from flask_migrate import Migrate
from tigerapp.config import CLOUD_NAME, API_KEY, API_SECRET, SENDGRID_API_KEY, DEFAULT_SENDER

app = Flask(__name__)

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

cloudinary.config( 
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret= API_SECRET,
    secure = True
)

mail_settings = {
    "MAIL_SERVER": 'smtp.sendgrid.net',
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USERNAME": 'apikey',
    "MAIL_PASSWORD": SENDGRID_API_KEY,
    'DEFAULT_SENDER': DEFAULT_SENDER
}

# ----------------------------------------------------------------------


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from tigerapp.main.routes import main
    from tigerapp.posts.routes import posts
    from tigerapp.users.routes import users
    from tigerapp.admin.routes import admin

    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(users)
    app.register_blueprint(admin)
    
    app.config.update(mail_settings)

    scheduler.init_app(app)
    scheduler_start()

    return app

from tigerapp.scheduler import scheduler, scheduler_start
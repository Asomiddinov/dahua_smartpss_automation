from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask import Flask
import os
from os import path
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
dir_path = os.path.dirname(os.path.realpath(__file__))
app.config.update(UPLOAD_PATH=os.path.join(dir_path, "static"))
app.config["SECRET_KEY"] = 'First time to log users out'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clients.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SESSION_TYPE'] = 'sqlalchemy'  # Or 'redis', 'filesystem', etc.
db.init_app(app)
migrate = Migrate(app, db, compare_type=True, render_as_batch=True)


def create_app():
    create_database(app)

    login_manager = LoginManager(app)
    login_manager.login_view = "login"
    login_manager.init_app(app)

    from forms import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app


with app.app_context():
    db.create_all()


def create_database(app):
    if not path.exists("instance/clients.db"):
        print("DB created!")

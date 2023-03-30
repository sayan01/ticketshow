from flask_login import *
from models import User
from app import app

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # type: ignore
login_manager.refresh_view = 'login' # type: ignore

@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    user = User.query.get(int(user_id))
    return user
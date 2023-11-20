from flask import Flask
from flask_migrate import Migrate

# internal importss
from config import Config
from .blueprints.site.routes import site
from .blueprints.auth.routes import auth
from .models import login_manager, db


app = Flask(__name__)

app.config.from_object(Config)

# ADD THIS
#wrap our app in login_manager so we can use it wherever in our app
login_manager.init_app(app)
login_manager.login_view = 'auth.sign_in' 
login_manager.login_message = "Hey you! Log in please!"
login_manager.login_message_category = 'warning'

app.register_blueprint(site)
app.register_blueprint(auth)

db.init_app(app)
migrate = Migrate(app,db)
from flask import Flask

from app_demandes.config import Config

app = Flask(__name__,template_folder='templates',static_folder='static')


app.config.from_object(Config)
from app_demandes import routes

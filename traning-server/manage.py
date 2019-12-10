from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from config import config
from app.db_models import db

app = Flask(__name__)
app.config.from_object(config['default'])
db.app = app
db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from app.db_models.models import *


if __name__ == '__main__':
    app.run()

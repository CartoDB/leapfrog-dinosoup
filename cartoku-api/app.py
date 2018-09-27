from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import JSON
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

## MODELS

class Deploy(db.Model):
    __tablename__ = 'deploys'

    id = db.Column(db.Integer, primary_key=True)
    app = db.Column(db.String())
    status = db.Column(db.String())

    def __init__(self, app, status):
        self.app = app
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)


## ROUTES

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/<username>/apps/<string:app_name>/deploy', methods=['POST'])
def show_deploy(app_name):
    status = request.form['status']
    deploy = Deploy(app_name, status)


@app.route('/<username>/deploys/<int:deploy_id>', methods=['GET'])
def show_deploy(deploy_id):

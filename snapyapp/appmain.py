from flask import Flask, request
from flask_restful import Resource, Api
from config.dbconfig import DbConfig

dbconfig = DbConfig.staging_config

app = Flask(__name__)
app.config.update(dbconfig)

from resources.signup import Signup

api = Api(app)
api.add_resource(Signup, '/signup')

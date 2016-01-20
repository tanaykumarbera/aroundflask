from flask import Flask, request
from flask_restful import Resource, Api
from config.dbconfig import DbConfig

dbconfig = DbConfig.staging_config

application = Flask(__name__)
application.config.update(dbconfig)

from resources.signup import Signup

api = Api(application)
api.add_resource(Signup, '/signup')

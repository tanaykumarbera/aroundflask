from flask import Flask, request
from flask_restful import Resource, Api
from config.dbconfig import DbConfig
from config.globalconfig import GlobalConfig

dbconfig = DbConfig.staging_config
globalconfig = GlobalConfig.staging_config

application = Flask(__name__)
application.config.update(dbconfig)
application.config.update(globalconfig)

from resources.signup import Signup
from resources.verifylogin import VerifyLogin
from resources.uploadimage import UploadImage
from resources.location import LocationApi
from resources.posts import Posts

api = Api(application)
api.add_resource(Signup, '/signup')
api.add_resource(VerifyLogin, '/verifylogin')
api.add_resource(UploadImage, '/uploadimage')
api.add_resource(LocationApi, '/location')
api.add_resource(Posts, '/posts')

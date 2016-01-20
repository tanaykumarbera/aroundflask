from flask import request, jsonify
from flask_restful import Resource, reqparse
from models.user import User
from models.token import Token
from models.device import Device
from models.appversion import AppVeriosn
from common.errorhandler import ErrorHandler


todos = {}

post_parser = reqparse.RequestParser(bundle_errors=True)
errorHandler = ErrorHandler()

post_parser.add_argument('fb_token', location='form', required=True, help='Facebook access token is required')
post_parser.add_argument('device_id', location='form', required=True, help='Device id is required')
post_parser.add_argument('device_name', location='form', help='')

class Signup(Resource):
	def post(self):
		args = post_parser.parse_args()
		userModel = User()
		tokenModel = Token()
		appVersion = AppVeriosn()
		minv, recentv = appVersion.getLatestVersion()
		user = userModel.isUserExist(args)
		if user:
			token_id = user.devices[0].token_id
			token = tokenModel.getTokenById(token_id)
			response = {"token" : token.token}
		else:
			deviceModel = Device()
			newUser = userModel.addUser(args)
			newToken = tokenModel.createNewToken()
			args['user_id'] = newUser.id
			args['token_id'] = newToken.id
			newDevice = deviceModel.addDevice(args)
			response = {"token" : newToken.token}
		response['min'] = minv
		response['recent'] = recentv
		return response, 200
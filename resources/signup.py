from flask import request, jsonify
from flask_restful import Resource, reqparse
from models.user import User
from models.token import Token
from models.device import Device
from models.appversion import AppVeriosn
from common.errorhandler import ErrorHandler

post_parser = reqparse.RequestParser(bundle_errors=True)
errorHandler = ErrorHandler()

post_parser.add_argument('fb_token', location='form', required=True, help='Facebook access token is required')
post_parser.add_argument('device_id', location='form', required=True, help='Device id is required')
post_parser.add_argument('device_name', location='form', help='')

class Signup(Resource):
	def post(self):
		response = dict()
		try :
			args = post_parser.parse_args()
			userModel = User()
			tokenModel = Token()
			deviceModel = Device()
			appVersion = AppVeriosn()
			minv, recentv = appVersion.getLatestVersion()
			user = userModel.isUserExist(args)
			if user:
				device = None
				for d in user.devices:
					if args['device_id'] == d.device_id:
						device = d
						break
				if device is None:
					token = tokenModel.createNewToken(args)
					args['user_id'] = user.id
					args['token_id'] = token.id
					newDevice = deviceModel.addDevice(args)
				else:
					device.token.updateToken(device.token.id, True, args)
					token = device.token
				response = {"token" : token.token}
			else:
				newUser = userModel.addUser(args)
				newToken = tokenModel.createNewToken(args)
				args['user_id'] = newUser.id
				args['token_id'] = newToken.id
				newDevice = deviceModel.addDevice(args)
				response = {"token" : newToken.token}

			response['min'] = minv
			response['recent'] = recentv
			return response, 200
		except Exception, e:
			response['message'] = str(e)
			return response, 400

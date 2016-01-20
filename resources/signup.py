from flask import request, jsonify
from flask_restful import Resource, reqparse
from models.user import User
from models.token import Token
from models.device import Device
from common.errorhandler import ErrorHandler


todos = {}

post_parser = reqparse.RequestParser(bundle_errors=True)
errorHandler = ErrorHandler()

post_parser.add_argument('fb_id', type=int, location='form', required=True, help='Facebook id is required')
post_parser.add_argument('fb_username', location='form', required=True, help='Facebook username is required')
post_parser.add_argument('fb_email', type=errorHandler.checkEmail, location='form', required=True, help='Facebook email is required')
post_parser.add_argument('fb_firstname', location='form', required=True, help='Firstname is required')
post_parser.add_argument('fb_lastname', location='form', required=True, help='Lastname is required')
post_parser.add_argument('fb_name', location='form', required=True, help='Full name is required')
post_parser.add_argument('fb_dp', location='form', help='')
post_parser.add_argument('fb_country', location='form', help='')
post_parser.add_argument('fb_gender', location='form', help='')
post_parser.add_argument('device_id', location='form', required=True, help='Device id is required')
post_parser.add_argument('device_name', location='form', help='')

class Signup(Resource):
	def post(self):
		args = post_parser.parse_args()
		userModel = User()
		tokenModel = Token()
		deviceModel = Device()
		user = userModel.isUserExist(args['fb_email'])
		if user:
			token_id = user.devices[0].token_id
			token = tokenModel.getTokenById(token_id)
			response = {"token" : token.token}
		else:
			newUser = userModel.addUser(args)
			newToken = tokenModel.createNewToken()
			args['user_id'] = newUser.id
			args['token_id'] = newToken.id
			newDevice = deviceModel.addDevice(args)
			response = {"token" : newToken.token}

		return response, 200
from flask import request, jsonify
from flask_restful import Resource, reqparse, fields, marshal
from models.user import User
from models.token import Token
from models.device import Device
from models.appversion import AppVeriosn
from common.utils import sqlAlchemyObjToDict

post_parser = reqparse.RequestParser(bundle_errors=True)

post_parser.add_argument('fb_token', location='form', required=True, help='Facebook access token is required')
post_parser.add_argument('device_id', location='form', required=True, help='Device id is required')
post_parser.add_argument('device_name', location='form', help='')


resource_fields = dict()
resource_fields['token'] = fields.String;
resource_fields['user'] = dict()
resource_fields['user']['first_name'] = fields.String(attribute='firstname')
resource_fields['user']['last_name'] = fields.String(attribute='lastname')
resource_fields['user']['gender'] = fields.String
resource_fields['user']['picture'] = fields.String(attribute='fb_dp')
resource_fields['app_version'] = dict()
resource_fields['app_version']['min'] = fields.String(attribute='min')
resource_fields['app_version']['recent'] = fields.String(attribute='recent')

class Signup(Resource):
	def post(self):
		data = dict()
		args = post_parser.parse_args()
		try :
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
				data = {"token" : token.token}
				user = sqlAlchemyObjToDict(user)
				data.update(user)
			else:
				newUser = userModel.addUser(args)
				newToken = tokenModel.createNewToken(args)
				args['user_id'] = newUser.id
				args['token_id'] = newToken.id
				newDevice = deviceModel.addDevice(args)
				data = {"token" : newToken.token}
				newUser = sqlAlchemyObjToDict(newUser)
				data.update(newUser)
			data['min'] = minv
			data['recent'] = recentv
			return marshal(data, resource_fields), 200
		except Exception, e:
			data['message'] = str(e)
			return data, 400

from flask import request, jsonify
from flask_restful import Resource, reqparse, fields, marshal
from datetime import datetime, timedelta
import requests

from models.user import User
from models.device import Device
from models.appversion import AppVeriosn
from common.errorhandler import ErrorHandler
from common.utils import sqlAlchemyObjToDict

post_parser = reqparse.RequestParser(bundle_errors=True)
errorHandler = ErrorHandler()

post_parser.add_argument('token', location='form', required=True, help='Token is required')
post_parser.add_argument('device_id', location='form', required=True, help='Device id id required')

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

class VerifyLogin(Resource):
	def post(self):
		data = dict()
		args = post_parser.parse_args()
		try :
			appVersion = AppVeriosn()
			minv, recentv = appVersion.getLatestVersion()
			deviceModel = Device()
			device = deviceModel.getDeviceByDeviceId(args)
			if args['token'] == device.token.token and datetime.now() < device.token.expiry:
				fb_url = "https://graph.facebook.com/me?access_token="+device.token.fb_token+"&fields=id,email,first_name,last_name,name,gender"
				res = requests.get(fb_url)
				if res.status_code == 200 :
					device.token.updateToken(device.token.id, False)
					data['token'] = device.token.token
					data['min'] = minv
					data['recent'] = recentv
					userModel = User()
					user = userModel.getUserById({'id' : device.user_id})
					user = sqlAlchemyObjToDict(user)
					data.update(user)
				else:
					raise Exception('Facebook access token is not valid.')
			else:
				raise Exception('Token is invalid or expired.')
			return marshal(data, resource_fields), 200
		except Exception, e:
			data['message'] = str(e)
			return data, 403
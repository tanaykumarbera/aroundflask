from flask import request, jsonify
from flask_restful import Resource, reqparse
from datetime import datetime, timedelta
import requests

from models.device import Device
from models.appversion import AppVeriosn
from common.errorhandler import ErrorHandler

post_parser = reqparse.RequestParser(bundle_errors=True)
errorHandler = ErrorHandler()

post_parser.add_argument('token', location='form', required=True, help='Token is required')
post_parser.add_argument('device_id', location='form', required=True, help='Device id id required')

class VerifyLogin(Resource):
	def post(self):
		response = dict()
		try :
			appVersion = AppVeriosn()
			minv, recentv = appVersion.getLatestVersion()
			args = post_parser.parse_args()
			deviceModel = Device()
			device = deviceModel.getDeviceByDeviceId(args)
			if args['token'] == device.token.token and datetime.now() < device.token.expiry:
				fb_url = "https://graph.facebook.com/me?access_token="+device.token.fb_token+"&fields=id,email,first_name,last_name,name,gender"
				res = requests.get(fb_url)
				if res.status_code == 200 :
					device.token.updateToken(device.token.id)
					response['token'] = device.token.token
					response['min'] = minv
					response['recent'] = recentv
				else:
					raise Exception('Facebook access token is not valid.')
			else:
				raise Exception('Token is invalid or expired.')
			return response, 200
		except Exception, e:
			response['message'] = str(e)
			return response, 403
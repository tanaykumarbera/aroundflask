from flask import request, jsonify
from flask_restful import Resource, reqparse
from common.models import Models
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
		models = Models()
		user = models.isUserExist(args['fb_email'])
		if user:
			userId = user['id']
		else:
			userId = models.addUser(args)
		response = {"newUserId" : userId}
		#return jsonify(response)
		del(models)
		return response, 200
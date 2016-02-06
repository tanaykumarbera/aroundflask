import os
from flask import request, jsonify
from flask_restful import Resource, reqparse, fields, marshal
from errormanager.errors import locationValidate, imageName, descriptionValidate, validateToken

from models.posts import Posts as PostsModel
from common.utils import ErrorWithCode

post_parser = reqparse.RequestParser(bundle_errors=True)

post_parser.add_argument('token', location='form', type=validateToken)
post_parser.add_argument('imagename', location='form', type=imageName)
post_parser.add_argument('lat_lng', location='form', type=locationValidate)
post_parser.add_argument('description', location='form', type=descriptionValidate)

class Posts(Resource):
	def post(self):
		data = dict()
		args = post_parser.parse_args()
		try:
			device = args['token']['device'] # Object
			location = args['lat_lng']['data'] # Dict
			lat_lng = args['lat_lng']['lat_lng']
			lat = lat_lng.split(',')[0].strip()
			lng = lat_lng.split(',')[1].strip()
			postParams = dict()
			postParams['user_id'] = device.user_id
			postParams['description'] = args['description']
			postParams['image_name'] = args['imagename']
			postParams['lat'] = lat
			postParams['lng'] = lng
			postParams['location_id'] = location['id']
			postModel = PostsModel()
			newPostId = postModel.addPost(postParams)
			data['id'] = newPostId
			return data, 200
		except Exception, e:
			data['message'] = str(e)
			return data, e.code if hasattr(e, 'code') else 500
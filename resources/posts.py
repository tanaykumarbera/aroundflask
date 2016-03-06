import os
from flask import request, jsonify
from flask_restful import Resource, reqparse, fields, marshal
from errormanager.errors import locationValidate, imageName, descriptionValidate, validateToken

from models.posts import Posts as PostsModel
from common.utils import ErrorWithCode

post_parser = reqparse.RequestParser(bundle_errors=True)

post_parser.add_argument('lat_lng', location=['form', 'args'], type=locationValidate)
post_parser.add_argument('token', location=['form', 'args'], type=validateToken)


class Posts(Resource):
	def post(self):
		post_parser.add_argument('imagename', location='form', type=imageName)
		post_parser.add_argument('description', location='form', type=descriptionValidate)
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
			postParams['location_id'] = location ? location['id'] : 0
			postModel = PostsModel()
			newPostId = postModel.addPost(postParams)
			data['id'] = newPostId
			return data, 200
		except Exception, e:
			data['message'] = str(e)
			return data, e.code if hasattr(e, 'code') else 500

	def get(self):
		post_parser.add_argument('not_ids', location='args', default='0')
		post_parser.add_argument('limits', location='args', default='10')
		post_parser.add_argument('feed_type', location='args', default='nearby')

		post_fields = dict()
		post_fields['post_id'] = fields.String(attribute='id');
		#post_fields['distance'] = fields.String(attribute='distance');
		post_fields['post_description'] = fields.String(attribute='description');
		post_fields['user_name'] = fields.String(attribute='user_name');
		post_fields['user_id'] = fields.String(attribute='user_id');
		post_fields['image_url'] = fields.String(attribute='image_url');
		post_fields['lat'] = fields.String(attribute='lat');
		post_fields['lng'] = fields.String(attribute='lng');
		post_fields['distance_in_kms'] = fields.String(attribute='distance_in_kms');
		post_fields['distance_in_miles'] = fields.String(attribute='distance_in_miles');

		list_post = dict()
		list_post['nearby'] = fields.List(fields.Nested(post_fields));

		args = post_parser.parse_args()
		try:
			device = args['token']['device'] # Object
			location = args['lat_lng']['data'] # Dict
			lat_lng = args['lat_lng']['lat_lng']
			lat = lat_lng.split(',')[0].strip()
			lng = lat_lng.split(',')[1].strip()
			getParams=dict()
			getParams['lat'] = lat
			getParams['lng'] = lng
			getParams['location_id'] = location['id']
			getParams['user_id'] = device.user_id
			getParams['not_ids'] = args['not_ids']
			getParams['limits'] = args['limits']
			postModel = PostsModel()
			if args['feed_type'] == "nearby":
				posts = postModel.getNearby(getParams)
			return marshal({'nearby': posts}, list_post), 200
		except Exception, e:
			data = dict()
			data['message'] = str(e)
			return data, e.code if hasattr(e, 'code') else 500
import os
from flask import request, jsonify
from flask_restful import Resource, reqparse, fields, marshal
from errormanager.errors import locationValidate, imageName, descriptionValidate, validateToken, validateTimeStamp, validateWhen

from models.posts import Posts as PostsModel
from common.utils import ErrorWithCode

post_parser = reqparse.RequestParser(bundle_errors=True)

post_parser.add_argument('lat_lng', location=['form', 'args'], type=locationValidate)
post_parser.add_argument('token', location=['form', 'args'], type=validateToken)

post_fields = dict()
post_fields['post_id'] = fields.String(attribute='id');
post_fields['post_description'] = fields.String(attribute='description');
post_fields['user_name'] = fields.String(attribute='user_name');
post_fields['user_id'] = fields.String(attribute='user_id');
post_fields['image_url'] = fields.String(attribute='image_url');
post_fields['lat'] = fields.String(attribute='lat');
post_fields['lng'] = fields.String(attribute='lng');
post_fields['distance_in_kms'] = fields.String(attribute='distance_in_kms');
post_fields['distance_in_miles'] = fields.String(attribute='distance_in_miles');
post_fields['distance'] = fields.String(attribute='distance');
post_fields['upvotes'] = fields.String(attribute='upvotes');
post_fields['downvotes'] = fields.String(attribute='downvotes');
post_fields['uservote'] = fields.String(attribute='uservote');
post_fields['self'] = fields.Boolean(attribute='self');

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
			postParams['location_id'] = location['id'] if location else 0
			postModel = PostsModel()
			newPost = postModel.addPost(postParams)
			return marshal(newPost, post_fields), 200
		except Exception, e:
			data['message'] = str(e)
			return data, e.code if hasattr(e, 'code') else 500

	def get(self):
		post_parser.add_argument('not_ids', location='args', default='0')
		post_parser.add_argument('limits', location='args', default='10')
		post_parser.add_argument('timestamp', location='args', type=validateTimeStamp)

		# When the value of when is before, it'll show posts happened before the timestamp
		# This is on infinite scroll
		# When the value of when is after, it'll show posts happened after the timestamp. i.e. New posts
		# This is on pull to refresh
		post_parser.add_argument('when', location='args', default='before', type=validateWhen)
		#post_parser.add_argument('feed_type', location='args', default='nearby')

		list_post = dict()
		list_post['posts'] = fields.List(fields.Nested(post_fields));

		args = post_parser.parse_args()
		#try:
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
		getParams['not_ids'] = '0' if args['not_ids']=='' else args['not_ids']
		getParams['limits'] = args['limits']
		getParams['timestamp'] = args['timestamp']
		getParams['when'] = args['when']

		postModel = PostsModel()
		posts = postModel.getNearby(getParams)
		return marshal({'posts': posts}, list_post), 200
		# except Exception, e:
		# 	data = dict()
		# 	data['message'] = str(e)
		# 	return data, e.code if hasattr(e, 'code') else 500
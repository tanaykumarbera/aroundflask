import os
from flask import request, jsonify
from flask_restful import Resource, reqparse, fields, marshal
from models.posts import Votes
from errormanager.errors import validateToken

post_parser = reqparse.RequestParser(bundle_errors=True)

post_parser.add_argument('post_id', location=['form', 'args'], type=int, required=True)
post_parser.add_argument('vote', location=['form', 'args'], type=int, required=True)
post_parser.add_argument('token', location=['form', 'args'], type=validateToken)

class Like(Resource):
	def post(self):
		data = dict()
		args = post_parser.parse_args()
		try:
			user_id = args['token']['device'].user_id
			post_id = args['post_id']
			vote = args['vote']
			VotesModel = Votes()
			VotesModel.addvote(user_id, post_id, vote);
			return data, 200
		except Exception, e:
			data['message'] = str(e)
			return data, e.code if hasattr(e, 'code') else 500
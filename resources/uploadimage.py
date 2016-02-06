import os
from flask import request
from flask_restful import Resource, reqparse, fields, marshal
import werkzeug
from datetime import datetime, timedelta
from md5 import md5

from models.device import Device
from common.utils import sqlAlchemyObjToDict, fileAllowed, ErrorWithCode


post_parser = reqparse.RequestParser(bundle_errors=True)


post_parser.add_argument('token', location='form', required=True, help='token is required')
post_parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files', required=True, help='image file is required')


class UploadImage(Resource):
	def put(self):
		data = dict()
		args = post_parser.parse_args()
		try:
			deviceModel = Device()
			device = deviceModel.getDevice(args)
			imgfile = args['image']
			ext = fileAllowed(imgfile.filename)
			if ext is None:
				raise ErrorWithCode(403, "File type not allowed")
			imagename = md5(datetime.now().strftime("%b%d%Y%h%m%s%f")).hexdigest()+"."+ext
			workingdir = os.getcwd()
			imgfile.save(os.path.join(workingdir,'images',imagename))
			data['imagename'] = imagename
			return data, 200
		except Exception, e:
			data['message'] = str(e)
			return data, e.code if hasattr(e, 'code') else 500
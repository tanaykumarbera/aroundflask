from flask import request
from flask_restful import Resource, reqparse, fields, marshal

from models.location import Location
from models.device import Device

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('token', location='args', required=True, help='Token is required.')
parser.add_argument('lat_lng', location='args', required=True, help='Location is required.')


location_fields = dict()
location_fields['name'] = fields.String(attribute='name');
location_fields['country'] = fields.String(attribute='country_name');
location_fields['country_code'] = fields.String(attribute='country_code');
location_fields['description'] = fields.String(attribute='description');
location_fields['coverimage'] = fields.String(attribute='coverimage');
location_fields['cdnurl'] = fields.String(attribute='cdnurl');

resource_fields = dict()
resource_fields['message'] = fields.String(attribute='message');
resource_fields['avllocation'] = fields.List(fields.Nested(location_fields));
resource_fields['inlocation'] = fields.Nested(location_fields);

class LocationApi(Resource):

	def get(self):
		data = dict()
		args = parser.parse_args()
		try:
			deviceModel = Device()
			device = deviceModel.getDevice(args)
			lat_lng = args['lat_lng']
			lat = lat_lng.split(',')[0].strip()
			lng = lat_lng.split(',')[1].strip()
			locationModel = Location()
			data['inlocation'] = locationModel.getLocationFromPosition({'lat':lat, 'lng':lng})
			data['avllocation'] = locationModel.getAllLocations()
			return marshal(data, resource_fields), 404 if data['inlocation'] is None else 200
		except Exception, e:
			data['message'] = str(e)
			return data, e.code if hasattr(e, 'code') else 500

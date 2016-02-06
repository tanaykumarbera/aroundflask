from models import db
from token import Token
from datetime import datetime
from common.utils import ErrorWithCode

class Device(db.Model):
	__tablename__ = 'device'

	id = 				db.Column(db.Integer, primary_key = True)
	device_id = 		db.Column(db.Unicode)
	device_name = 		db.Column(db.Unicode)
	user_id = 			db.Column(db.Integer, db.ForeignKey('user.id'))
	add_date = 			db.Column(db.DateTime)
	token_id = 			db.Column(db.Integer, db.ForeignKey(Token.id))
	last_logged_in = 	db.Column(db.DateTime)
	token = 			db.relationship('Token', uselist=False)


	def addDevice(self, params):
		self.device_name = params['device_name'] if 'device_name' in params else None
		self.device_id = params['device_id']
		self.user_id = params['user_id']
		self.token_id = params['token_id']
		db.session.add(self)
		db.session.commit()
		return self

	def getDeviceByDeviceId(self, params):
		device = self.query.filter_by(device_id=params['device_id']).first()
		if device is None:
			raise ErrorWithCode(404, "This device is not signed up before")
		return device

	def getDevice(self, params):
		device = None
		if 'token' in params:
			device = self.query.join(Token).filter(Token.token==params['token']).filter(datetime.now() < Token.expiry).first()
		if device is None:
			raise ErrorWithCode(401, "This token is not valid.")
		return device
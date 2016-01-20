from models import db

class Device(db.Model):
	__tablename__ = 'device'

	id = 				db.Column(db.Integer, primary_key = True)
	device_id = 		db.Column(db.Unicode)
	device_name = 		db.Column(db.Unicode)
	user_id = 			db.Column(db.Integer, db.ForeignKey('user.id'))
	add_date = 			db.Column(db.DateTime)
	token_id = 			db.Column(db.Integer, db.ForeignKey('token.id'))
	last_logged_in = 	db.Column(db.DateTime)


	def addDevice(self, params):
		self.device_name = params['device_name'] if 'device_name' in params else None
		self.device_id = params['device_id']
		self.user_id = params['user_id']
		self.token_id = params['token_id']
		db.session.add(self)
		db.session.commit()
		return self
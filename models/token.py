from models import db
from datetime import datetime, timedelta
from md5 import md5
from device import Device

class Token(db.Model):
	__tablename__ = 'token'

	id = 	 	db.Column(db.Integer, primary_key = True)
	token =  	db.Column(db.Unicode)
	expiry = 	db.Column(db.DateTime)
	devices = 	db.relationship('Device', backref='token', lazy='select')

	def createNewToken(self):
		self.token = md5(datetime.now().strftime("%b%d%Y%h%m%s%f")).hexdigest()
		self.expiry = datetime.now() + timedelta(days=10)
		db.session.add(self)
		db.session.commit()
		return self

	def getTokenById(self, id):
		token = self.query.get(id)
		return token
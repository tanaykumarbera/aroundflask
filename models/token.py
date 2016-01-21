from models import db
from datetime import datetime, timedelta
from md5 import md5
from device import Device

class Token(db.Model):
	__tablename__ = 'token'

	id = 	 	db.Column(db.Integer, primary_key = True)
	token =  	db.Column(db.Unicode)
	fb_token =  db.Column(db.Text)
	expiry = 	db.Column(db.DateTime)
	devices = 	db.relationship('Device', backref='token', lazy='select')

	def createNewToken(self, params):
		self.token = md5(datetime.now().strftime("%b%d%Y%h%m%s%f")).hexdigest()
		self.fb_token = params['fb_token']
		self.expiry = datetime.now() + timedelta(days=10)
		db.session.add(self)
		db.session.commit()
		return self

	def getTokenById(self, id):
		token = self.query.get(id)
		return token

	def getToken(self, token):
		token = self.query.filter_by(token=token)

	def updateFbToken(self, token_id, params):
		token = self.query.get(token_id)
		token.fb_token = params['fb_token']
		db.session.commit()
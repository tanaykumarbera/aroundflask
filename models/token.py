from models import db
from datetime import datetime, timedelta
from md5 import md5

class Token(db.Model):
	__tablename__ = 'token'

	id = 	 	db.Column(db.Integer, primary_key = True)
	token =  	db.Column(db.Unicode)
	fb_token =  db.Column(db.Text)
	expiry = 	db.Column(db.DateTime)

	def createNewToken(self, params):
		self.token = md5(datetime.now().strftime("%b%d%Y%h%m%s%f")).hexdigest()
		self.fb_token = params['fb_token']
		self.expiry = datetime.now() + timedelta(days=60)
		db.session.add(self)
		db.session.commit()
		return self

	def getTokenById(self, id):
		token = self.query.get(id)
		return token

	def getToken(self, token):
		token = self.query.filter_by(token=token)

	def updateToken(self, token_id, params=dict()):
		token = self.query.get(token_id)
		if 'fb_token' in params:
			token.fb_token = params['fb_token']
		token.expiry = datetime.now() + timedelta(days=60)
		token.token = md5(datetime.now().strftime("%b%d%Y%h%m%s%f")).hexdigest()
		db.session.commit()
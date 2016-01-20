from models import db
from device import Device
import requests
import json

class User(db.Model):
	__tablename__ = 'user'

	id = 		db.Column(db.Integer, primary_key = True)
	fb_id = 	db.Column(db.Integer)
	fb_dp = 	db.Column(db.Text)
	email = 	db.Column(db.Unicode)
	firstname = db.Column(db.Unicode)
	lastname = 	db.Column(db.Unicode)
	name = 		db.Column(db.Unicode)
	gender = 	db.Column(db.Unicode)
	add_date = 	db.Column(db.DateTime)
	devices = 	db.relationship('Device', backref='user', lazy='select')

	userDetails = dict()

	def isUserExist(self, params):
		if 'fb_token' in params:
			self.setUserDetailFromFacebook(params['fb_token'])
			return self.isUserExist({'email': self.userDetails['email']})
		elif 'email' in params:
			user = self.query.filter_by(email=params['email']).first()
		else:
			user = None
		return user

	def addUser(self, params):
		if 'fb_token' in params:
			return self.addUser(self.userDetails)
		else:
			self.fb_id = params['fb_id']
			self.fb_dp = params['fb_dp']
			self.email = params['email']
			self.firstname = params['firstname']
			self.lastname = params['lastname']
			self.name = params['name']
			self.gender = params['gender']
		db.session.add(self)
		db.session.commit()
		return self

	def setUserDetailFromFacebook(self, fb_token):
		fb_url = "https://graph.facebook.com/me?access_token="+fb_token+"&fields=id,email,first_name,last_name,name,gender"
		res = requests.get(fb_url)
		res = json.loads(res.text)
		self.userDetails['fb_id'] = res['id']
		self.userDetails['fb_dp'] = "http://graph.facebook.com/"+str(res['id'])+"/picture?type=large"
		self.userDetails['email'] = res['email']
		self.userDetails['firstname'] = res['first_name']
		self.userDetails['lastname'] = res['last_name']
		self.userDetails['name'] = res['name']
		self.userDetails['gender'] = res['gender']


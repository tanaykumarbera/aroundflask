from models import db
from device import Device

class User(db.Model):
	__tablename__ = 'user'

	id = 			db.Column(db.Integer, primary_key = True)
	fb_id = 		db.Column(db.Integer)
	fb_username = 	db.Column(db.Unicode)
	fb_email = 		db.Column(db.Unicode)
	fb_firstname = 	db.Column(db.Unicode)
	fb_lastname = 	db.Column(db.Unicode)
	fb_name = 		db.Column(db.Unicode)
	fb_dp = 		db.Column(db.Text)
	fb_country = 	db.Column(db.Unicode)
	fb_gender = 	db.Column(db.Unicode)
	add_date = 		db.Column(db.DateTime)
	devices = 		db.relationship('Device', backref='user', lazy='select')


	def isUserExist(self, email):
		user = self.query.filter_by(fb_email=email).first()
		return user

	def addUser(self, params):
		self.fb_id = params['fb_id']
		self.fb_username = params['fb_username']
		self.fb_email = params['fb_email']
		self.fb_firstname = params['fb_firstname']
		self.fb_lastname = params['fb_lastname']
		self.fb_name = params['fb_name']
		self.fb_dp = params['fb_dp']
		self.fb_country = params['fb_country']
		self.fb_gender = params['fb_gender']

		db.session.add(self)
		db.session.commit()
		return self
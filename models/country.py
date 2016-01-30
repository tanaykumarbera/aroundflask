from models import db
from location import Location

class Location(db.Model):
	__tablename__ = 'country'

	id = 				db.Column(db.Integer, primary_key = True)
	name = 				db.Column(db.Unicode)
	code = 				db.Column(db.Unicode)
	devices = 			db.relationship('Location', backref='country', lazy='select')


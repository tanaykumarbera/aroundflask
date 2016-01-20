from models import db
from sqlalchemy import desc

class AppVeriosn(db.Model):
	__tablename__ = 'appversion'

	id = 		db.Column(db.Integer, primary_key = True)
	min = 		db.Column(db.Unicode)
	recent = 	db.Column(db.Unicode)
	add_date = 	db.Column(db.DateTime)

	def getLatestVersion(self):
		row = self.query.order_by(desc(self.id)).one()
		return row.min, row.recent
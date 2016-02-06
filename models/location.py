from models import db
from sqlalchemy import text
from common.utils import sqlAlchemyProxyObjToDict

class Location(db.Model):
	__tablename__ = 'location'

	id = 			db.Column(db.Integer, primary_key = True)
	country_id = 	db.Column(db.Integer)
	description = 	db.Column(db.Text)
	coverimage = 	db.Column(db.Text)
	cdnurl = 		db.Column(db.Text)

	def getLocationFromPosition(self, params):
		sql = ("SELECT l.id, l.name, l.description, l.coverimage, l.cdnurl, c.name AS country_name, c.code AS country_code "
				"FROM  `location` l,  `country` c "
				"WHERE CONTAINS( l.polygon, GEOMFROMTEXT(  'POINT({0} {1})' ) ) "
				"AND l.country_id = c.id")
		sql = text(sql.format(params['lat'], params['lng']))
		results = db.engine.execute(sql)
		for row in results:
			return sqlAlchemyProxyObjToDict(row, ['id', 'name', 'description', 'coverimage', 'cdnurl', 'country_code', 'country_name'])
		return None

	def getAllLocations(self):
		sql = ("SELECT l.id, l.name, l.description, l.coverimage, l.cdnurl, c.name AS country_name, c.code AS country_code "
				"FROM  `location` l,  `country` c "
				"WHERE l.country_id = c.id "
				"ORDER BY c.id")
		sql = text(sql)
		print sql
		results = db.engine.execute(sql)
		locations = list()
		for row in results:
			locations.append(sqlAlchemyProxyObjToDict(row, ['id', 'name', 'description', 'coverimage', 'cdnurl', 'country_code', 'country_name']))
		return locations
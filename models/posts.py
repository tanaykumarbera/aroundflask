from models import db
from sqlalchemy import text
from common.utils import sqlAlchemyProxyObjToDict, getDistance

class Posts(db.Model):
	__tablename__ = 'posts'

	id = 			db.Column(db.Integer, primary_key = True)
	user_id = 		db.Column(db.Integer)
	description = 	db.Column(db.Text)
	image_name = 	db.Column(db.Text)
	location_id = 	db.Column(db.Integer)

	def addPost(self, params):
		sql = ("INSERT INTO `posts` "
				"(`id`, `user_id`, `description`, `image_name`, `latlng`, `location_id`, `rank`, `add_date`) "
				"VALUES (NULL, '{0}', '{1}', '{2}', GeomFromText('POINT({3} {4})',0), '{5}', '0', CURRENT_TIMESTAMP) "
			)
		sql = text(sql.format(params['user_id'], params['description'], params['image_name'], params['lat'], params['lng'], params['location_id']))
		post = db.engine.execute(sql)
		return post.lastrowid

	def getNearby(self, params):
		sql = ("SELECT `p`.`id`, ("
				"GLENGTH( LINESTRINGFROMWKB( LINESTRING("
				"`p`.`latlng`, GEOMFROMTEXT( 'POINT({0} {1})' ) ) ) )"
				") AS distance, "
				"`p`.`description`, "
				"X(`p`.`latlng`) AS lat, "
				"Y(`p`.`latlng`) AS lng, "
				"`u`.`name`AS user_name, "
				"`u`.`id` AS user_id, "
				"CONCAT(`l`.`cdnurl`,`p`.`image_name`) AS image_url "
				"FROM posts p, user u, location l "
				"WHERE `p`.`id` NOT IN ({2}) "
				"AND `l`.`id` = {3} "
				"AND `p`.`user_id` = `u`.`id` "
				"ORDER BY distance ASC "
				"LIMIT {4}"
			)
		sql = text(sql.format(params['lat'], params['lng'], params['not_ids'], params['location_id'], params['limits']))
		rows = db.engine.execute(sql)
		posts = list()
		for post in rows:
			postDict = sqlAlchemyProxyObjToDict(post, ['id', 'distance', 'description', 'user_name', 'user_id', 'image_url', 'lat', 'lng'])
			m = getDistance(str(params['lat'])+","+str(params['lng']), str(postDict['lat'])+","+str(postDict['lng']))
			km = float(m)/1000
			km = "%2f"%km
			ml = float(m)/1609.34
			ml = "%2f"%ml
			postDict['distance_in_kms'] = km
			postDict['distance_in_miles'] = ml
			posts.append(postDict)
		return posts

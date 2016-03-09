from models import db
from sqlalchemy import text
from common.utils import sqlAlchemyProxyObjToDict, getDistance

class Posts(db.Model):
	__tablename__ = 'post'

	id = 			db.Column(db.Integer, primary_key = True)
	user_id = 		db.Column(db.Integer)
	description = 	db.Column(db.Text)
	image_name = 	db.Column(db.Text)
	location_id = 	db.Column(db.Integer)

	def addPost(self, params):
		sql = ("INSERT INTO `post` "
				"(`id`, `user_id`, `description`, `image_name`, `latlng`, `location_id`, `rank`, `add_date`) "
				"VALUES (NULL, '{0}', '{1}', '{2}', GeomFromText('POINT({3} {4})',0), '{5}', '0', CURRENT_TIMESTAMP) "
			)
		sql = text(sql.format(params['user_id'], params['description'], params['image_name'], params['lat'], params['lng'], params['location_id']))
		post = db.engine.execute(sql)
		return post.lastrowid

	def getNearby(self, params):
		sql = ("SELECT * FROM "
				"(SELECT `p`.`id`, ("
				"GLENGTH( LINESTRINGFROMWKB( LINESTRING("
				"`p`.`latlng`, GEOMFROMTEXT( 'POINT({0} {1})' ) ) ) )"
				") AS distance, "
				"`p`.`description`, "
				"X(`p`.`latlng`) AS lat, "
				"Y(`p`.`latlng`) AS lng, "
				"`u`.`name`AS user_name, "
				"`u`.`id` AS user_id, "
				"CONCAT(`l`.`cdnurl`,`p`.`image_name`) AS image_url "
				"FROM post p, user u, location l "
				"WHERE `p`.`id` NOT IN ({2}) "
				"AND `l`.`id` = {3} "
				"AND `p`.`user_id` = `u`.`id` "
				"ORDER BY distance ASC LIMIT 100) "
				"AS t1 "
				"WHERE t1.distance < 1 "
				"LIMIT {4}"
			)
		# Check the third param location id
		# Plan changed to get rid of locations
		# So did this
		# Will be changed later
		# This will just help to get cdn url
		sql = text(sql.format(params['lat'], params['lng'], params['not_ids'], 1, params['limits']))
		print sql
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
			print postDict
			posts.append(postDict)
		return posts

class Votes(db.Model):
	__tablename__ = 'votes'

	id = 		db.Column(db.Integer, primary_key = True)
	user_id = 	db.Column(db.Integer)
	post_id = 	db.Column(db.Integer)
	vote = 		db.Column(db.Boolean)

	def addvote(self, user_id, post_id, vote):
		vote = self.query.filter_by(and_(user_id==user_id, post_id==post_id)).first()
		if vote is None:
			self.user_id = user_id
			self.post_id = post_id
			self.vote = vote
			db.session.add(self)
		else:
			vote.vote = vote
		db.session.commit()

	def removevote(self, user_id, post_id):
		self.query.filter_by(and_(user_id==user_id, post_id==post_id)).delete()

	def getpostvote(self, post_id, user_id=0):
		if user_id is 0:
			user_vote = 0
		else:
			vote = self.query.filter_by(and_(posts_id==user_id, post_id==post_id)).first()
			if vote is None:
				user_vote = 0
			else:
				if vote.vote is True:
					user_vote = 1
				else:
					user_vote = -1
		upvotes = self.query.filter_by(and_(post_id==post_id, vote==True)).count()
		downvotes = self.query.filter_by(and_(post_id==post_id, vote==False)).count()
		return upvotes, downvotes, user_vote





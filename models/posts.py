from models import db
from sqlalchemy import text, and_
from common.utils import sqlAlchemyProxyObjToDict, getDistance

class Posts(db.Model):
	__tablename__ = 'post'

	id = 			db.Column(db.Integer, primary_key = True)
	user_id = 		db.Column(db.Integer)
	description = 	db.Column(db.Text)
	image_name = 	db.Column(db.Text)
	location_id = 	db.Column(db.Integer)

	def addPost(self, params):

		# According to our ranking algorithm
		# rank of an intial post is always
		# 0.2871745887492588

		sql = text("INSERT INTO `post` "
				"(`id`, `user_id`, `description`, `image_name`, `latlng`, `location_id`, `rank`, `add_date`) "
				"VALUES (NULL, :user_id, :description, :image_name, GeomFromText(:point, 0), :location_id, '0.2871745887492588', CURRENT_TIMESTAMP) "
			)
		#sql = text(sql.format(params['user_id'], params['description'], params['image_name'], params['lat'], params['lng'], params['location_id']))

		post = db.engine.execute(sql,
									user_id=params['user_id'],
									description=params['description'],
									image_name=params['image_name'],
									point='POINT('+str(params['lat'])+' '+str(params['lng'])+')',
									location_id=params['location_id'])
		post_id = post.lastrowid

		# Make a positivie vote from the user him/herself
		voteModel = Votes()
		voteModel.addvote(params['user_id'], post_id, 1)

		getPostParams = dict();
		getPostParams['lat'] = params['lat']
		getPostParams['lng'] = params['lng']
		getPostParams['id'] = post_id

		return self.getPostById(getPostParams)

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

				"FROM post p, user u, location l "

				"WHERE `p`.`id` NOT IN ({2}) "
				"{5}"
				"AND `l`.`id` = {3} "
				"AND `p`.`user_id` = `u`.`id` "
				"AND  GLENGTH(LINESTRINGFROMWKB(LINESTRING(`p`.`latlng`, GEOMFROMTEXT('POINT({0} {1})')))) < 1 "

				"ORDER BY `p`.`rank` DESC, distance ASC LIMIT {4} "
			)

		timestampCond = ''
		if params['when'] == 'before':
			timestampCond = "AND `p`.`add_date` <= '"+str(params['timestamp']+"' ")
		else:
			timestampCond = "AND `p`.`add_date` > '"+str(params['timestamp']+"' ")

		# Check the third param location id
		# Plan changed to get rid of locations
		# So did this
		# Will be changed later
		# This will just help to get cdn url
		sql = text(sql.format(params['lat'], params['lng'], params['not_ids'], 1, params['limits'], timestampCond))
		print sql
		rows = db.engine.execute(sql)
		posts = list()
		for post in rows:
			posts.append(self.createPostDict(post, params))
		return posts

	def getPostById(self, params):
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
				"FROM post p, user u, location l "
				"WHERE `p`.`id` = ({2}) "
			)

		sql = text(sql.format(params['lat'], params['lng'], params['id']))
		print sql
		rows = db.engine.execute(sql)
		posts = list()
		voteModel = Votes()
		for post in rows:
			posts.append(self.createPostDict(post, params))
		return posts[0]

	def createPostDict(self, post, params):
		postDict = sqlAlchemyProxyObjToDict(post, ['id', 'distance', 'description', 'user_name', 'user_id', 'image_url', 'lat', 'lng'])
		if 'user_id' in params:
			m = getDistance(str(params['lat'])+","+str(params['lng']), str(postDict['lat'])+","+str(postDict['lng']))
			km = float(m)/1000
			km = "%2f"%km
			ml = float(m)/1609.34
			ml = "%2f"%ml
			voteModel = Votes()
			postDict['distance_in_kms'] = km
			postDict['distance_in_miles'] = ml
			postDict['upvotes'], postDict['downvotes'], postDict['uservote'] = voteModel.getpostvote(postDict['id'], params['user_id'])
		else:
			# Coming from add post
			postDict['distance_in_kms'] = '0.000000'
			postDict['distance_in_miles'] = '0.000000'
			postDict['upvotes'], postDict['downvotes'], postDict['uservote'] = 1, 0, 1
		return postDict


class Votes(db.Model):
	__tablename__ = 'votes'

	id = 		db.Column(db.Integer, primary_key = True)
	user_id = 	db.Column(db.Integer)
	post_id = 	db.Column(db.Integer)
	vote = 		db.Column(db.Integer)

	# vote value should be 1 or -1
	def addvote(self, user_id, post_id, vote):
		voteRow = self.query.filter(Votes.user_id==user_id, Votes.post_id==post_id).one_or_none()
		if voteRow is None:
			self.user_id = user_id
			self.post_id = post_id
			self.vote = vote
			db.session.add(self)
		else:
			if(voteRow.vote == vote):
				db.session.delete(voteRow)
			else:
				voteRow.vote = vote
		db.session.commit()



	# returns total number of upvotes, downvotes and user's vote
	def getpostvote(self, post_id, user_id=0):
		if user_id is 0:
			user_vote = 0
		else:
			vote = self.query.filter(Votes.user_id==user_id, Votes.post_id==post_id).one_or_none()
			if vote is None:
				user_vote = 0
			else:
				user_vote = vote.vote
		upvotes = self.query.filter(Votes.post_id==post_id, Votes.vote==1).count()
		downvotes = self.query.filter(Votes.post_id==post_id, Votes.vote==-1).count()
		return upvotes, downvotes, user_vote





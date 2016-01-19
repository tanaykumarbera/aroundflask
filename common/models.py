import MySQLdb.cursors
from config.dbconfig import DbConfig

class Models:
	def __init__(self):
		config = DbConfig.staging_config
		self.db = MySQLdb.connect( 	host = config['MYSQL_DATABASE_HOST'],
									user = config['MYSQL_DATABASE_USER'],
									passwd = config['MYSQL_DATABASE_PASSWORD'],
									db = config['MYSQL_DATABASE_DB'],
									cursorclass=MySQLdb.cursors.DictCursor
								)
	def __del__(self):
		self.db.close()

	def addUser (self, userParams):
		params = []
		fileds = []
		for p in userParams:
			if p.startswith('fb'):
				fileds.append(p)
				params.append(userParams[p])
		params = tuple(params)
		fileds = ",".join(fileds)
		sql = """INSERT INTO user("""+fileds+""") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
		user_id = 0
		cursor = self.db.cursor()
		try:
			cursor.execute(sql, params)
			self.db.commit()
			user_id = cursor.lastrowid
		except:
			self.db.rollback()
		return user_id

	def isUserExist (self, email):
		sql = """SELECT * FROM user WHERE fb_email = %s"""
		cursor = self.db.cursor()
		params = tuple([email])
		cursor.execute(sql, params)
		result = cursor.fetchone()
		return result

	def addDevice (self, deviceParams):
		pass

	def createToken (self):
		pass
from models import db
from sqlalchemy import text
from common.utils import sqlAlchemyProxyObjToDict

class Posts(db.Model):
	__tablename__ = 'posts'

	id = 			db.Column(db.Integer, primary_key = True)
	user_id = 		db.Column(db.Integer)
	description = 	db.Column(db.Text)
	image_name = 	db.Column(db.Text)
	location_id = 	db.Column(db.Integer)

	def addPost(self, params):
		sql = ("INSERT INTO `posts` "
				"(`id`, `use_id`, `description`, `image_name`, `latlng`, `location_id`, `rank`, `add_date`) "
				"VALUES (NULL, '{0}', '{1}', '{2}', GeomFromText('POINT({3} {4})',0), '{5}', '0', CURRENT_TIMESTAMP) "
			)
		sql = text(sql.format(params['user_id'], params['description'], params['image_name'], params['lat'], params['lng'], params['location_id']))
		post = db.engine.execute(sql)
		return post.lastrowid
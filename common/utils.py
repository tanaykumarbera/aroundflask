def sqlAlchemyObjToDict(sqlalchemyobj):
	d = {}
	for column in sqlalchemyobj.__table__.columns:
		d[column.name] = str(getattr(sqlalchemyobj, column.name))
	return d

def sqlAlchemyProxyObjToDict(sqlalchemyobj, columns):
	d = {}
	for column in columns:
		d[column] = str(getattr(sqlalchemyobj, column))
	return d

def fileAllowed(filename):
	ext = filename.split('.')[-1].lower()
	allowedExts = ['jpg', 'jpeg', 'png']
	if ext in allowedExts:
		return ext
	else:
		return None

class ErrorWithCode(Exception):
	errors = dict()
	errors['304'] = 'Not Modified'
	errors['400'] = 'Bad Request'
	errors['401'] = 'Unauthorized'
	errors['403'] = 'Forbidden'
	errors['404'] = 'Not Found'

	def __init__(self, code, msg=None):
		self.code = code
		self.msg = msg if msg is not None else self.errors[repr(code)]
	def __str__(self):
		return self.msg
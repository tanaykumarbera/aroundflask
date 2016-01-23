def sqlAlchemyObjToDict(sqlalchemyobj):
	d = {}
	for column in sqlalchemyobj.__table__.columns:
		d[column.name] = str(getattr(sqlalchemyobj, column.name))
	return d
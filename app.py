from flask import Flask, request
from flask_restful import Resource, Api

from resources.signup import Signup

app = Flask(__name__)
api = Api(app)

api.add_resource(Signup, '/signup')

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)

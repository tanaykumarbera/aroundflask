from flask import Flask
application = Flask(__name__)

@application.route("/")
def hello():
	return "<h1> Wow This is Working </h1>"

if __name__ == "__main__":
	application.run(host='0.0.0.0')

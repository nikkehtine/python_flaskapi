from flask import Flask

from api import setup_api_routes
from extensions import api, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

setup_api_routes(api)
db.init_app(app)
api.init_app(app)


@app.route("/")
def hello():
	return "<h1>Hello from python-flaskapi!</h1>"


if __name__ == "__main__":
	app.run(debug=True)

from flask import Flask
from flask_restful import Api, Resource, abort, fields, marshal_with, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
api = Api(app)

user_fields = {
	"id": fields.Integer,
	"name": fields.String,
	"email": fields.String,
}


class UserModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)

	def __repr__(self):
		return f"User(name = {self.name}, email = {self.email})"


user_args = reqparse.RequestParser()
user_args.add_argument(
	"name", type=str, required=True, help="Name cannot be blank"
)
user_args.add_argument(
	"email", type=str, required=True, help="Email cannot be blank"
)


class Users(Resource):
	@marshal_with(user_fields)
	def get(self):
		users = UserModel.query.all()
		return users

	@marshal_with(user_fields)
	def post(self):
		args = user_args.parse_args()
		user = UserModel(name=args["name"], email=args["email"])
		db.session.add(user)
		db.session.commit()
		users = UserModel.query.all()
		return users, 201


class User(Resource):
	@marshal_with(user_fields)
	def get(self, user_id):
		user = UserModel.query.filter_by(id=user_id).first()
		if not user:
			abort(404, message="User not found")
		return user

	@marshal_with(user_fields)
	def patch(self, user_id):
		args = user_args.parse_args()
		user = UserModel.query.filter_by(id=user_id).first()
		if not user:
			abort(404, message="User not found")
		user.name = args["name"]
		user.email = args["email"]
		db.session.commit()
		return user

	@marshal_with(user_fields)
	def delete(self, user_id):
		user = UserModel.query.filter_by(id=user_id).first()
		if not user:
			abort(404, message="User not found")
		db.session.delete(user)
		db.session.commit()
		users = UserModel.query.all()
		return users


api.add_resource(Users, "/api/users")
api.add_resource(User, "/api/users/<int:user_id>")


@app.route("/api/coffee")
def coffee():
	return "", 418


@app.route("/")
def hello():
	return "<h1>Hello from python-flaskapi!</h1>"


if __name__ == "__main__":
	app.run(debug=True)

import uuid

from flask_restful import Resource, abort, fields, marshal_with, reqparse
from werkzeug.security import generate_password_hash

from extensions import db

user_fields = {
	"public_id": fields.String,
	"name": fields.String,
	"email": fields.String,
}


def get_user_by_id(user_id):
	user = UserModel.query.filter_by(id=user_id).first()
	return user


def get_user_by_public_id(public_id):
	user = UserModel.query.filter_by(public_id=public_id).first()
	return user


class UserModel(db.Model):
	__tablename__ = "user_account"
	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(50), unique=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(120), nullable=False)
	admin = db.Column(db.Boolean, default=False)

	def __repr__(self):
		return f"User(name={self.name}, email={self.email})"


class TodoModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(100), nullable=False)
	complete = db.Column(db.Boolean, default=False)
	user_id = db.Column(
		db.Integer, db.ForeignKey("user_account.id"), nullable=False
	)
	user = db.relationship("UserModel", backref=db.backref("todos", lazy=True))
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())


class Users(Resource):
	@marshal_with(user_fields)
	def get(self):
		users = UserModel.query.all()
		return users

	@marshal_with(user_fields)
	def post(self):
		args = user_args.parse_args()

		hashed_password = generate_password_hash(
			args["password"], method="scrypt"
		)

		user = UserModel(
			public_id=str(uuid.uuid4()),
			name=args["name"],
			email=args["email"],
			password=hashed_password,
			admin=False,
		)
		db.session.add(user)
		db.session.commit()

		created_user = get_user_by_id(user.id)
		return created_user, 201


class User(Resource):
	@marshal_with(user_fields)
	def get(self, public_id):
		user = get_user_by_public_id(public_id)
		if not user:
			abort(404, message="User not found")
		return user

	@marshal_with(user_fields)
	def patch(self, public_id):
		args = user_args.parse_args()
		user = get_user_by_public_id(public_id)
		if not user:
			abort(404, message="User not found")
		user.name = args["name"]
		user.email = args["email"]
		db.session.commit()
		return user

	def delete(self, public_id):
		user = get_user_by_public_id(public_id)
		if not user:
			abort(404, message="User not found")
		db.session.delete(user)
		db.session.commit()
		return "", 204


user_args = reqparse.RequestParser()
user_args.add_argument(
	"name", type=str, required=True, help="Name cannot be blank"
)
user_args.add_argument(
	"email", type=str, required=True, help="Email cannot be blank"
)
user_args.add_argument(
	"password", type=str, required=True, help="Password cannot be blank"
)

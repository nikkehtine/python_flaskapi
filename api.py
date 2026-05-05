from flask import Blueprint

from extensions import api
from users import User, Users

users_bp = Blueprint("users", __name__, url_prefix="/api")

api.add_resource(Users, "/api/users")
api.add_resource(User, "/api/users/<string:public_id>")


@users_bp.route("/coffee")
def coffee():
	return "", 418

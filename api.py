from flask_restful import Resource

from users import User, Users


class Coffee(Resource):
	def get(self):
		return "", 418


def setup_api_routes(api):
	api.add_resource(Users, "/api/users")
	api.add_resource(User, "/api/users/<string:public_id>")
	api.add_resource(Coffee, "/api/coffee")

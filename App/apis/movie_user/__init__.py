from flask_restful import Api

from App.apis.movie_user.movie_user_api_ import MovieUsersResource
from App.apis.movie_user.movie_order_api import MovieOrdersResource, MovieOrderResource

client_api = Api(prefix='/user')

client_api.add_resource(MovieUsersResource, '/movieusers/')
client_api.add_resource(MovieOrdersResource,'/movieorders/')
client_api.add_resource(MovieOrderResource,'/movieorders/<int:order_id>/')

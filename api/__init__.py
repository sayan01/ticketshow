from app import app
from flask_restful import Api
from .show import *
from .venue import *

api = Api(app)

api.add_resource(ShowList, '/api/shows')
api.add_resource(ShowDetail, '/api/shows/<int:id>')

api.add_resource(VenueList, '/api/venues')
api.add_resource(VenueDetail, '/api/venues/<int:id>')
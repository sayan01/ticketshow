from flask import request
from flask_restful import Resource, fields, marshal_with, reqparse, marshal, abort
from models import Venue, Show, Booking, User, db

venue_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'address': fields.String,
    'city': fields.String,
    'capacity': fields.Integer,
}

venue_parser = reqparse.RequestParser()
venue_parser.add_argument('name', type=str, required=True, help='Name of the venue is required')
venue_parser.add_argument('address', type=str, required=True, help='Address of the venue is required')
venue_parser.add_argument('city', type=str, required=True, help='City of the venue is required')
venue_parser.add_argument( 'capacity', type=int, required=True, help='Capacity of the venue is required')

class VenueList(Resource):
    @marshal_with(venue_fields)
    def get(self):
        venues = Venue.query.all()
        return venues, 200

    @marshal_with(venue_fields)
    def post(self):
        args = venue_parser.parse_args()
        if args['capacity'] < 0:
            abort(400, message="Capacity should be non-negative")
        venue = Venue(name=args['name'], address=args['address'],
                      city=args['city'].upper(), capacity=args['capacity'])
        db.session.add(venue)
        db.session.commit()
        return venue, 201

class VenueDetail(Resource):
    @marshal_with(venue_fields)
    def get(self, id):
        venue = Venue.query.get(id)
        if not venue:
            abort(404, message="Venue {} doesn't exist".format(id))
        return venue, 200

    @marshal_with(venue_fields)
    def put(self, id):
        venue = Venue.query.get(id)
        if not venue:
            abort(404, message="Venue {} doesn't exist".format(id))
        args = venue_parser.parse_args()
        if args['capacity'] < 0:
            abort(400, message="Capacity should be non-negative")
        venue.name = args['name']
        venue.address = args['address']
        venue.city = args['city']
        venue.capacity = args['capacity']
        db.session.commit()
        return venue, 201

    def delete(self, id):
        venue = Venue.query.get(id)
        if not venue:
            abort(404, message="Venue {} doesn't exist".format(id))
        for show in venue.shows:
            for booking in show.bookings:
                db.session.delete(booking)
            db.session.delete(show)
        db.session.delete(venue)
        db.session.commit()
        return '', 204

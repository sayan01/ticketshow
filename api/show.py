from flask import request
from flask_restful import Resource, fields, marshal_with, reqparse, marshal, abort
from models import Venue, Show, Booking, User, db
from datetime import datetime

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

class MyDateFormat(fields.Raw):
    def format(self, value):
        return value.strftime(DATE_TIME_FORMAT)


show_fields = {
    'id': fields.Integer,
    'venue_id': fields.Integer,
    'name': fields.String,
    'rating': fields.Float,
    'start_time': MyDateFormat,
    'end_time': MyDateFormat,
    'price': fields.Float,
    'tags': fields.String,
}

show_parser = reqparse.RequestParser()
show_parser.add_argument('venue_id', type=int, required=True, help='Venue ID is required')
show_parser.add_argument('name', type=str, required=True, help='Name of the show is required')
show_parser.add_argument('rating', type=float, required=True, help='Rating of the show is required')
show_parser.add_argument('start_time', type=str, required=True, help='Start time of the show is required')
show_parser.add_argument('end_time', type=str, required=True, help='End time of the show is required')
show_parser.add_argument('price', type=float, required=True, help='Price of the show is required')
show_parser.add_argument('tags', type=str, required=True, help='Tags of the show is required')

class ShowList(Resource):
    @marshal_with(show_fields)
    def get(self):
        shows = Show.query.all()
        return shows, 200

    @marshal_with(show_fields)
    def post(self):
        args = show_parser.parse_args()
        if not Venue.query.get(args['venue_id']):
            abort(404, message="Venue {} doesn't exist".format(args['venue_id']))
        if args['rating'] not in range(1, 6):
            abort(400, message="Rating should be between 1 and 5")
        try:
            args['start_time'] = datetime.strptime(args['start_time'], DATE_TIME_FORMAT)
            args['end_time'] = datetime.strptime(args['end_time'], DATE_TIME_FORMAT)
        except ValueError:
            abort(400, message="Invalid time format, should be: " + DATE_TIME_FORMAT)
        if args['start_time'] > args['end_time']:
            abort(400, message="Start time should be before end time")
        if args['start_time'] < datetime.now():
            abort(400, message="Start time should be in the future")
        if args['start_time'].date() != args['end_time'].date():
            abort(400, message="Start time and end time should be on the same day")
        # check if show overlaps with another show
        c1 = Show.query.filter(Show.venue_id == args['venue_id'],
            Show.start_time <= args['start_time'],
            Show.end_time >= args['start_time']).first()
        c2 = Show.query.filter(Show.venue_id == args['venue_id'],
            Show.start_time <= args['end_time'],
            Show.end_time >= args['end_time']).first()
        c3 = Show.query.filter(Show.venue_id == args['venue_id'],
            Show.start_time >= args['start_time'],
            Show.end_time <= args['end_time']).first()
        c4 = Show.query.filter(Show.venue_id == args['venue_id'],
            Show.start_time <= args['start_time'],
            Show.end_time >= args['end_time']).first()
        if c1 or c2 or c3 or c4:
            abort(400, message="Show overlaps with another show")
        if args['price'] < 0:
            abort(400, message="Price should be non-negative")
        if args['tags'] and args['tags'] != '':
            args['tags'] = ",".join([t.strip() for t in args['tags'].split(',')])
        show = Show(venue_id=args['venue_id'], name=args['name'],
                    rating=args['rating'], start_time=args['start_time'],
                    end_time=args['end_time'], price=args['price'],
                    tags=args['tags'])
        db.session.add(show)
        db.session.commit()
        return show, 201

class ShowDetail(Resource):
    @marshal_with(show_fields)
    def get(self, id):
        show = Show.query.get(id)
        if not show:
            abort(404, message="Show {} doesn't exist".format(id))
        return show, 200

    @marshal_with(show_fields)
    def put(self, id):
        show = Show.query.get(id)
        if not show:
            abort(404, message="Show {} doesn't exist".format(id))
        args = show_parser.parse_args()
        if not Venue.query.get(args['venue_id']):
            abort(404, message="Venue {} doesn't exist".format(args['venue_id']))
        if args['rating'] not in range(1, 6):
            abort(400, message="Rating should be between 1 and 5")
        try:
            args['start_time'] = datetime.strptime(args['start_time'], DATE_TIME_FORMAT)
            args['end_time'] = datetime.strptime(args['end_time'], DATE_TIME_FORMAT)
        except ValueError:
            abort(400, message="Invalid time format, should be: " + DATE_TIME_FORMAT)
        if args['start_time'] > args['end_time']:
            abort(400, message="Start time should be before end time")
        # if args['start_time'] < datetime.now():
        #     abort(400, message="Start time should be in the future")
        if args['start_time'].date() != args['end_time'].date():
            abort(400, message="Start time and end time should be on the same day")
        # check if show overlaps with another show
        c1 = Show.query.filter(Show.venue_id == args['venue_id'],
            Show.id != id,
            Show.start_time <= args['start_time'],
            Show.end_time >= args['start_time']).first()
        c2 = Show.query.filter(Show.venue_id == args['venue_id'],
            Show.id != id,
            Show.start_time <= args['end_time'],
            Show.end_time >= args['end_time']).first()
        c3 = Show.query.filter(Show.venue_id == args['venue_id'],
            Show.id != id,
            Show.start_time >= args['start_time'],
            Show.end_time <= args['end_time']).first()
        c4 = Show.query.filter(Show.venue_id == args['venue_id'],
            Show.id != id,
            Show.start_time <= args['start_time'],
            Show.end_time >= args['end_time']).first()
        if c1 or c2 or c3 or c4:
            abort(400, message="Show overlaps with another show")
        if args['price'] < 0:
            abort(400, message="Price should be non-negative")
        if args['tags'] and args['tags'] != '':
            args['tags'] = ",".join([t.strip() for t in args['tags'].split(',')])
        show.venue_id = args['venue_id']
        show.name = args['name']
        show.rating = args['rating']
        show.start_time = args['start_time']
        show.end_time = args['end_time']
        show.price = args['price']
        show.tags = args['tags']
        db.session.commit()
        return show, 201

    def delete(self, id):
        show = Show.query.get(id)
        if not show:
            abort(404, message="Show {} doesn't exist".format(id))
        for booking in show.bookings:
            db.session.delete(booking)
        db.session.delete(show)
        db.session.commit()
        return '', 204
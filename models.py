# Models

import datetime

from sqlalchemy import DateTime

from appconfig import db


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String)
    facebook_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String)
    image_link = db.Column(db.String)
    created_date = db.Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def short_serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Venue(Base):
    __tablename__ = 'Venue'

    address = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Venue Id: {self.id}, Venue Name: {self.name}>'

    @property
    def venue_details(self):
        import helpers
        past_shows = helpers.get_past_shows_at_venue(self.id)
        upcoming_shows = helpers.get_upcoming_shows_at_venue(self.id)
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_talent': self.seeking_talent,
            'image_link': self.image_link,
            'past_shows': [show.artist_serializer for show in past_shows],
            'upcoming_shows': [show.artist_serializer for show in upcoming_shows],
            'past_shows_count': len(past_shows),
            'seeking_description': self.seeking_description,
            'upcoming_shows_count': len(upcoming_shows),
        }

    @property
    def venue_location_serializer(self):
        return {
            'city': self.city,
            'state': self.state
        }


class Artist(Base):
    __tablename__ = 'Artist'

    seeking_venue = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Artist Id: {self.id}, Artist Name: {self.name}>'

    @property
    def artist_details(self):
        import helpers
        past_shows = helpers.get_past_shows_of_artist(self.id)
        upcoming_shows = helpers.get_upcoming_shows_of_artist(self.id)
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,
            'past_shows': [show.venue_serializer for show in past_shows],
            'upcoming_shows': [show.venue_serializer for show in upcoming_shows],
            'past_shows_count': len(past_shows),
            'upcoming_shows_count': len(upcoming_shows),
        }


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime())
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    artist = db.relationship('Artist', backref=db.backref('Show', cascade="all,delete"))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    venue = db.relationship('Venue', backref=db.backref('Show', cascade="all,delete"))
    created_date = db.Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Show Id: {self.id}, Artist: {self.artist}>, Venue Id: {self.venue}'

    @property
    def artist_serializer(self):
        return {
            'artist_id': self.artist_id,
            'artist_name': self.artist.name,
            'artist_image_link': self.artist.image_link,
            'start_time': str(self.start_time)
        }

    @property
    def venue_serializer(self):
        return {
            'venue_id': self.venue_id,
            'venue_name': self.venue.name,
            'venue_image_link': self.venue.image_link,
            'start_time': str(self.start_time)
        }

    @property
    def show_details(self):
        return {
            'venue_id': self.venue_id,
            'venue_name': self.venue.name,
            'artist_id': self.artist_id,
            'artist_name': self.artist.name,
            'artist_image_link': self.artist.image_link,
            'start_time': str(self.start_time)
        }

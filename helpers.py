# Helper Methods

from datetime import datetime

from models import Venue, Show, db, Artist

def get_venues_by_distinct_locations() -> list:
    """
    Returns a list of Venues by distinct locations
    :return: List of Venue objects
    """
    return Venue.query.distinct(Venue.city, Venue.state).all()


def get_venues_by_location(city, state) -> list:
    """
    Returns list of venues filtered by city and state
    :param city: name of city
    :param state: name of state
    :return: List of Venue object
    """
    return Venue.query.filter_by(city=city, state=state).all()


def get_past_shows_at_venue(venue_id) -> list:
    """
    Returns list of Past shows at the Venue
    :param venue_id: Venue id (pk)
    :return: List of Venue object
    """
    return db.session.query(Show).filter(Show.start_time < datetime.now(), Show.venue_id == venue_id).all()


def get_upcoming_shows_at_venue(venue_id) -> list:
    """
    Returns list of Upcoming shows at the Venue
    :param venue_id: Venue id (pk)
    :return: List of Venue object
   """
    return db.session.query(Show).filter(Show.start_time > datetime.now(), Show.venue_id == venue_id).all()


def get_past_shows_of_artist(artist_id) -> list:
    """
    Returns list of Past shows for the Artist
    :param artist_id: Artist id (pk)
    :return: List of Artist Objects
    """
    return db.session.query(Show).filter(Show.start_time <= datetime.now(), Show.artist_id == artist_id).all()


def get_upcoming_shows_of_artist(artist_id) -> list:
    """
    Returns list of Upcoming shows for the Artist
    :param artist_id: Artist id (pk)
    :return: List of Artist Objects
    """
    return db.session.query(Show).filter(Show.start_time > datetime.now(), Show.artist_id == artist_id).all()


def get_venue_by_id(venue_id) -> Venue:
    """
    Return Venue object corresponding to the Id
    :param venue_id: Venue id (pk)
    :return: Venue object
    """
    return Venue.query.filter_by(id=venue_id).first_or_404()


def get_artist_by_id(artist_id) -> Artist:
    """
    Returns Artist identified by the artist id
    :param artist_id: Artist id (pk)
    :return: Artist object
    """
    return Artist.query.filter_by(id=artist_id).first_or_404()


def search_venue(search_term) -> list:
    """
    Searches venue by partial text. Venues are searched by name.
    :param search_term: Search term with which we want to search
    :return: List of Venue
    """
    return Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()


def search_artist(search_term) -> list:
    """
    Searches artist by partial text. Artists are searched by name.
    :param search_term: Search term
    :return: List of Artist objects
    """
    return Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()


def get_show_by_id(show_id) -> Show:
    """
    Returns Show identified by the show id
    :param show_id: Show id (pk)
    :return: Show object
    """
    return Show.query.filter_by(id=show_id).first_or_404()


def search_show(search_term) -> list:
    """
    Searches show by partial text. Checks for Venues/Artists names matching that partial text
    :param search_term: Search term with which we want to search
    :return: List of shows
    """
    return Show.query.filter(
        Show.artist.has(Artist.name.ilike(f'%{search_term}%')) | Show.venue.has(
            Venue.name.ilike(f'%{search_term}%'))).all()

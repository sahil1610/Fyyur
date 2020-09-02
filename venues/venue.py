from flask import Blueprint, render_template, flash, request, redirect, url_for

from appconfig import db
from forms import VenueForm
from helpers import get_venues_by_distinct_locations, get_venues_by_location, get_venue_by_id, search_venue
from models import Venue

venue = Blueprint('venue', __name__, template_folder='templates')


@venue.route('/venues')
def venues():
    """
    Handler to display the list of all venues grouped by City and State
    :return: Rendered template to show all venues
    """
    # find all venues on the basis of distinct city and states
    venues_by_locations = get_venues_by_distinct_locations()
    data = []
    if venues_by_locations:
        # prepare data to be displayed in the template
        data = [v.venue_location_serializer for v in venues_by_locations]
        for venue_data in data:
            venue_data['venues'] = get_venues_by_location(venue_data['city'], venue_data['state'])
            venue_data['venue_count'] = len(venue_data['venues'])
    return render_template('pages/venues.html', areas=data)


@venue.route('/venues/search', methods=['POST'])
def search_venues():
    """
    Search Venue Post handler. Search venues by venue name partial text match
    :return: Rendered template to show the test results
    """
    search_term = request.form.get('search_term', '')
    # search venue by venue name partial match
    venues_by_text = search_venue(search_term)
    # prepare data to shown in the template
    response = {
        'count': len(venues_by_text),
        'data': [v.short_serializer for v in venues_by_text]
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@venue.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    """
    Handler to show a specific Venue
    :param venue_id: Id of the Venue
    :return: Rendered Show venue template
    """
    data = get_venue_by_id(venue_id).venue_details
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@venue.route('/venues/create', methods=['GET'])
def create_venue_form():
    """
    Create Venue Form Get handler. Opens the create venue form
    :return: Rendered New Venue template
    """
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@venue.route('/venues/create', methods=['POST'])
def create_venue_submission():
    """
    Venue creation Post handler.  Message is flashed on success and failure
    :return: Rendered home page template
    """
    form = VenueForm(request.form)

    try:
        new_venue = Venue(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            address=form.address.data,
            phone=form.phone.data,
            genres=form.genres.data,
            facebook_link=form.facebook_link.data,
            image_link=form.image_link.data,
            website=form.website.data,
            seeking_talent=form.seeking_talent.data,
            seeking_description=form.seeking_description.data
        )

        db.session.add(new_venue)
        db.session.commit()

        flash('Venue ' + request.form['name'] + ' was successfully listed!', 'info')

    except Exception as ex:
        db.session.rollback()
        flash('Error occurred. Venue ' + request.form['name'] + ' could not be listed. ' + str(ex), 'danger')
    finally:
        db.session.close()

    return redirect(url_for('index'))


@venue.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    """
    Delete handler for the Venue. Message is flashed on success and failure
    :param venue_id: Id of the Venue to be deleted
    :return: Rendered home page template
    """
    try:
        venue_to_be_deleted = Venue.query.get(venue_id)
        venue_name = venue_to_be_deleted.name
        # delete the venue
        db.session.delete(venue_to_be_deleted)
        db.session.commit()
        flash('Venue ' + venue_name + ' was successfully deleted!', 'info')
    except:
        db.session.rollback()
        flash('Error occurred. Venue could not be deleted.', 'danger')
    finally:
        db.session.close()

    return redirect(url_for('index'))


@venue.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    """
    Edit Venue Get handler. Opens the Edit filled form
    :param venue_id: Id if the venue to be edited
    :return: Rendered Edit Venue Template
    """
    form = VenueForm()
    venue_to_be_edited = get_venue_by_id(venue_id)
    form.state.process_data(venue_to_be_edited.state)
    form.genres.process_data(venue_to_be_edited.genres)
    return render_template('forms/edit_venue.html', form=form, venue=venue_to_be_edited)


@venue.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    """
    Edit Venue post handler. If the event is updated success message is flashed and if the same fails failure message
    sis flashed along with the failure reason
    :param venue_id: Venue id to edited
    :return: Rendered Home Page Template
    """
    try:
        # update the Venue details and save it to DB
        form = VenueForm(request.form)
        venue_to_be_edited = get_venue_by_id(venue_id)
        name = form.name.data

        venue_to_be_edited.name = name
        venue_to_be_edited.genres = form.genres.data
        venue_to_be_edited.city = form.city.data
        venue_to_be_edited.state = form.state.data
        venue_to_be_edited.address = form.address.data
        venue_to_be_edited.phone = form.phone.data
        venue_to_be_edited.facebook_link = form.facebook_link.data
        venue_to_be_edited.website = form.website.data
        venue_to_be_edited.image_link = form.image_link.data
        venue_to_be_edited.seeking_talent = form.seeking_talent.data
        venue_to_be_edited.seeking_description = form.seeking_description.data

        db.session.commit()
        flash('Venue ' + name + ' was successfully updated!', 'info')
    except Exception:
        # In case of exception flash an error and rollback the transaction
        db.session.rollback()
        flash('An error occurred. Venue with id ' + str(venue_id) + ' could not be updated.', 'danger')
    finally:
        db.session.close()

    return redirect(url_for('venue.show_venue', venue_id=venue_id))

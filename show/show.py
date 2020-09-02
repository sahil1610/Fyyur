from flask import Blueprint, render_template, flash, request, redirect, url_for

from appconfig import db
from forms import ShowForm
from helpers import search_show
from models import Show, Artist, Venue

show = Blueprint('show', __name__, template_folder='templates')


@show.route('/shows')
def shows():
    """
    Handler to show all shows
    :return: Rendered template to display all shows
    """
    all_shows = Show.query.all()
    # prepare data for template
    data = [s.show_details for s in all_shows]
    return render_template('pages/shows.html', shows=data)


@show.route('/show/create')
def create_shows():
    """
    Handler to open the create show form
    :return: Rendered Create show form
    """
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@show.route('/show/create', methods=['POST'])
def create_show_submission():
    """
    Create show submission Post handler. Creates a new show and message is flashed on successful creation or in case of
    failure
    :return: Rendered home page template
    """
    form = ShowForm()
    artist_id = form.artist_id.data
    venue_id = form.venue_id.data
    error = False
    try:
        if Artist.query.get(artist_id) and Venue.query.get(venue_id):
            new_show = Show(
                artist_id=form.artist_id.data,
                venue_id=form.venue_id.data,
                start_time=form.start_time.data,
            )
            db.session.add(new_show)
            db.session.commit()

            flash('Show was successfully listed!', 'info')
        else:
            error = True
    except Exception as ex:
        db.session.rollback()
        flash('Error occurred. Show could not be listed.' + str(ex), 'danger')
    finally:
        db.session.close()

    if error:
        flash(
            'Unable to create a show as Artist with artist_id "' + artist_id + '" or Venue with venue_id "' + venue_id
            + '" doesn\'t exist', 'danger')

    return redirect(url_for('index'))


@show.route('/shows/search', methods=['POST'])
def search_shows():
    """
    Search show Post handler. Searches shows by partial text match on artist name or virtual name
    :return: Rendered template to display search results
    """
    search_term = request.form.get('search_term', '')
    shows_searched = search_show(search_term)
    response = {
        'count': len(shows_searched),
        'data': [s.show_details for s in shows_searched]
    }

    print(response)
    return render_template('pages/show.html', results=response,
                           search_term=request.form.get('search_term', ''))

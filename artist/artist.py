from flask import Blueprint, render_template, redirect, url_for, request, flash

from appconfig import db
from forms import ArtistForm
from helpers import get_artist_by_id, search_artist
from models import Artist

artist = Blueprint('artist', __name__, template_folder='templates')


@artist.route('/artists')
def artists():
    """
    Handler to show all artists
    :return: Rendered artists page template displaying all artists
    """
    all_artists = Artist.query.all()
    data = [a.short_serialize for a in all_artists]
    return render_template('pages/artists.html', artists=data)


@artist.route('/artists/search', methods=['POST'])
def search_artists():
    """
    Search Artist Post handler. Searches artist by partial text match on Artist name
    :return: Rendered tenplate showing search results
    """
    search_term = request.form.get('search_term', '')
    artists_by_text = search_artist(search_term)
    response = {
        'count': len(artists_by_text),
        'data': [a.short_serialize for a in artists_by_text]
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@artist.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    """
    SHow artist page handler
    :param artist_id:  Id of the artist
    :return: Rendered show artist template
    """
    data = get_artist_by_id(artist_id).artist_details
    return render_template('pages/show_artist.html', artist=data)


@artist.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    """
    Edit artist Get handler. Opens the filled edit artist page
    :param artist_id: Id of the artist to be edited
    :return: Rendered filled edit artist template
    """
    form = ArtistForm()
    artist_to_be_edited = get_artist_by_id(artist_id)
    form.state.process_data(artist_to_be_edited.state)
    form.genres.process_data(artist_to_be_edited.genres)
    return render_template('forms/edit_artist.html', form=form, artist=artist_to_be_edited)


@artist.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    """
    Edit artist Post handler. Message is flashed on success and failure
    :param artist_id: Id of the artist to be edited
    :return: rendered home page template
    """
    try:
        form = ArtistForm(request.form)
        artist_to_be_edited = get_artist_by_id(artist_id)

        artist_name = form.name.data

        artist_to_be_edited.name = artist_name
        artist_to_be_edited.genres = form.genres.data
        artist_to_be_edited.city = form.city.data
        artist_to_be_edited.state = form.state.data
        artist_to_be_edited.phone = form.phone.data
        artist_to_be_edited.facebook_link = form.facebook_link.data
        artist_to_be_edited.website = form.website.data
        artist_to_be_edited.image_link = form.image_link.data
        artist_to_be_edited.seeking_venue = form.seeking_venue.data
        artist_to_be_edited.seeking_description = form.seeking_description.data

        db.session.commit()
        flash('Artist ' + artist_name + ' was successfully updated!', 'info')
    except Exception as ex:
        db.session.rollback()
        flash('An error occurred. Artist with id ' + str(artist_id) + ' could not be updated.' + str(ex), 'danger')
    finally:
        db.session.close()

    return redirect(url_for('artist.show_artist', artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------

@artist.route('/artists/create', methods=['GET'])
def create_artist_form():
    """
    Create artist Get handler. Open the create artist page
    :return: Rendered create artist templated
    """
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@artist.route('/artists/create', methods=['POST'])
def create_artist_submission():
    """
    Create artist post handler. Message is flashed on success and failure
    :return: Rendered home page template
    """
    form = ArtistForm()
    try:
        if form.validate:
            new_artist = Artist(
                name=form.name.data,
                genres=form.genres.data,
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                image_link=form.image_link.data,
                facebook_link=form.facebook_link.data,
                website=form.website.data,
                seeking_venue=form.seeking_venue.data,
                seeking_description=form.seeking_description.data
            )
            db.session.add(new_artist)
            db.session.commit()

            flash('Artist ' + form.name.data + ' was successfully listed!', 'info')
    except Exception as ex:
        db.session.rollback()
        flash('Error occurred. Artist ' + form.name.data + ' could not be listed.' + str(ex), 'danger')
    finally:
        db.session.close()

    return redirect(url_for('index'))


@artist.route('/artists/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    """
    Delete artist handler. Message is flashed on success and failure
    :param artist_id: Id of the artist to be deleted
    :return: Rendered home page template
    """
    try:
        artist_to_be_deleted = get_artist_by_id(artist_id)
        artist_name = artist_to_be_deleted.name
        # delete the artist
        db.session.delete(artist_to_be_deleted)
        db.session.commit()
        flash('Artist ' + artist_name + ' was successfully deleted!', 'info')
    except Exception as ex:
        db.session.rollback()
        flash('Error occurred. Artist could not be deleted. ' + str(ex), 'danger')
    finally:
        db.session.close()

    return redirect(url_for('index'))

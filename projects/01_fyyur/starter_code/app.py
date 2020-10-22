#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    artists = db.relationship("Artist", secondary="shows")
    genres = db.relationship("Genre", backref=db.backref("venue", cascade="all, delete", lazy=True))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    # genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    venues = db.relationship("Venue", secondary="shows")
    genres = db.relationship("Genre", backref=db.backref("artist", cascade="all, delete", lazy=True))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column( db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column( db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    start_time = db.Column( db.String, nullable=False)

    artists = db.relationship("Artist", backref=db.backref("shows", cascade="all, delete", lazy=True))
    venues = db.relationship("Venue", backref=db.backref("shows", cascade="all, delete", lazy=True))

class Genre(db.Model):
  __tablename__ = 'genres'
  id= db.Column(db.Integer, primary_key=True)
  name = db.Column( db.String, nullable=False)
  venue_id = db.Column( db.Integer, db.ForeignKey('Venue.id'), nullable=True)
  artist_id = db.Column( db.Integer, db.ForeignKey('Artist.id'), nullable=True)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  locations=db.session.query(Venue.city, Venue.state).group_by(Venue.city).group_by(Venue.state).all()
  data=[]
  for locData in locations:
    arr={
      "city": locData[0],
      "state": locData[1]
    }
    vArr=[]
    venues = db.session.query(Venue).filter_by(city=locData[0], state=locData[1]).all()
    for v in venues:
      num_upcoming_shows = len(v.shows)
      vArr.append({
        "id": v.id,
        "name": v.name,
        "num_upcoming_shows": num_upcoming_shows,
      })
    arr["venues"]= vArr
    data.append(arr)

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search = "%{}%".format(request.form.get("search_term"))
  venues = Venue.query.filter(Venue.name.ilike(search)).all()
  count=0
  data=[]
  for v in venues:
    shows=v.shows
    count=0
    for sh in shows:
        date_time_obj = datetime.datetime.strptime(sh.start_time, '%Y-%m-%d %H:%M:%S')
        if date_time_obj>datetime.datetime.now():
          count = count+1
    data.append({
      "id": v.id,
      "name": v.name,
      "num_upcoming_shows": count
    })
  response={
    "count": len(venues),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  upcoming_shows=[]
  past_shows= db.session.query(Artist.id, Artist.name, Artist.image_link, Show.start_time).join(Show).filter_by(venue_id=venue_id).all()
  pShows=[]
  uShows=[]
  for item in past_shows:
    date_time_obj = datetime.datetime.strptime(item[3], '%Y-%m-%d %H:%M:%S')
    if date_time_obj<datetime.datetime.now():
      pShows.append({
        "artist_id": item[0],
        "artist_name": item[1],
        "artist_image_link": item[2],
        "start_time": item[3]
      })
    else:
      uShows.append({
        "artist_id": item[0],
        "artist_name": item[1],
        "artist_image_link": item[2],
        "start_time": item[3]
      })

  genres=db.session.query(Genre.name).filter(Genre.venue_id==venue.id).all()
  gList=[]
  for g in genres:
    gList.append(g.name)
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": gList,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": "https://www.themusicalhop.com",
    "facebook_link": venue.facebook_link,
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": venue.image_link,
    "past_shows": pShows,
    "upcoming_shows": uShows,
    "past_shows_count": len(pShows),
    "upcoming_shows_count": len(uShows),
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion
  error = False
  try:
    venue = request.form
    v = Venue()
    v.name = venue.get("name")
    v.city = venue.get("city")
    v.state = venue.get("state")
    v.address = venue.get("address")
    v.phone = venue.get("phone")
    genList = venue.getlist("genres")
    genreL = []
    for g in genList:
      gen = Genre()
      gen.name = g
      genreL.append(gen)
    print(genreL)
    v.genres=genreL
    v.image_link = venue.get("image_link")
    v.facebook_link = venue.get("facebook_link")
    db.session.add(v)
    db.session.commit()
  except:
    sys.exc_info()
    db.session.rollback()
    error = True
  finally:
    db.session.close()

  # on successful db insert, flash success
  if not error:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # DONE: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # DONE: replace with real data returned from querying the database
  data=Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search = "%{}%".format(request.form.get("search_term"))
  artists = Artist.query.filter(Artist.name.ilike(search)).all()
  count=0
  data=[]
  for v in artists:
    shows=v.shows
    count=0
    for sh in shows:
        date_time_obj = datetime.datetime.strptime(sh.start_time, '%Y-%m-%d %H:%M:%S')
        if date_time_obj>datetime.datetime.now():
          count = count+1
    data.append({
      "id": v.id,
      "name": v.name,
      "num_upcoming_shows": count
    })
  response={
    "count": len(artists),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.get(artist_id)
  
  past_shows= db.session.query(Venue.id, Venue.name, Venue.image_link, Show.start_time).join(Show).filter_by(artist_id=artist_id).all()
  
  pShows=[]
  uShows=[]
  for item in past_shows:
    date_time_obj = datetime.datetime.strptime(item[3], '%Y-%m-%d %H:%M:%S')
    if date_time_obj<datetime.datetime.now():
      pShows.append({
        "venue_id": item[0],
        "venue_name": item[1],
        "venue_image_link": item[2],
        "start_time": item[3]
      })
    else:
      uShows.append({
        "venue_id": item[0],
        "venue_name": item[1],
        "venue_image_link": item[2],
        "start_time": item[3]
      })
  
  genres=db.session.query(Genre.name).filter(Genre.artist_id==artist.id).all()
  gList=[]
  for g in genres:
    gList.append(g.name)
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": gList,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": artist.facebook_link,
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": artist.image_link,
    "past_shows": pShows,
    "upcoming_shows": uShows,
    "past_shows_count": len(pShows),
    "upcoming_shows_count": len(uShows),
  }
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion
  error = False
  try:
    artist = request.form
    a = Artist()
    a.name = artist.get("name")
    a.city = artist.get("city")
    a.state = artist.get("state")
    a.address = artist.get("address")
    a.phone = artist.get("phone")
    genList = artist.getlist("genres")
    genreL = []
    for g in genList:
      gen = Genre()
      gen.name = g
      genreL.append(gen)
    a.genres=genreL
    a.image_link = artist.get("image_link")
    a.facebook_link = artist.get("facebook_link")
    db.session.add(a)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()

  # on successful db insert, flash success
  if not error:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  
  # on successful db insert, flash success
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # Done: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  res=db.session.query(Show.start_time, Venue.id, Venue.name, Artist.id, Artist.name, Artist.image_link).join(Venue).filter(Venue.id==Show.venue_id).join(Artist).filter(Artist.id==Show.artist_id).all()
  data=[]
  for x in res:
    data.append({
    "venue_id": x[1],
    "venue_name": x[2],
    "artist_id": x[3],
    "artist_name": x[4],
    "artist_image_link": x[5],
    "start_time": x[0]
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # DONE: insert form data as a new Show record in the db, instead
  error=False
  try:
    show = Show()
    showF = request.form
    print(showF)
    show.artist_id = showF.get("artist_id")
    show.venue_id = showF.get("venue_id")
    show.start_time = showF.get("start_time")
    db.session.add(show)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()
  # on successful db insert, flash success
  if not error:
    flash('Show was successfully listed!')
  else:
    flash('An error occurred. Show could not be listed.')
  # flash('Show was successfully listed!')
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

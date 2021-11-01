import os, json, datetime
from flask import Flask, render_template, request, url_for, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

import streamfinder.database as db

def run_website():

  template_folder = os.path.join(os.path.dirname(__file__), 'templates')
  static_folder = os.path.join(os.path.dirname(__file__), 'static')
  print("using template folder %s" % template_folder)
  print("using static folder %s" % static_folder)

  app = Flask(__name__,
    template_folder=template_folder,
    static_url_path='/static',
    static_folder=static_folder)

  app.config['SECRET_KEY'] = "It's a secret to everybody..."

  ### Main Page ###
  @app.route('/')
  def index():
    userID = session.get('userID')
    if userID is None:
       return render_template_wrapper('index.html', variable_from_python="Hello, anonymous user!")

    user = db.Database().getUser(int(userID))
    return render_template_wrapper('index.html', variable_from_python="Hello, " + user.getUsername() + "!")

  ### Login / Register Page ###
  @app.route('/auth', methods=['GET'])
  def auth():
    userID = session.get('userID')
    if userID is not None:
      return redirect(url_for('index'))
    return render_template_wrapper('authentication.html')

  ### Handle Login Request ###
  @app.route('/auth/login', methods=['POST'])
  def login():
    database = db.Database()
    username = request.form.get("username")
    password = request.form.get("password")
    userToLogin = database.searchUserByUsername(username)

    if not userToLogin:
      # There is no account associated with this username
      return render_template_wrapper('authentication.html', status="There is no account associated with this username.")
    elif not check_password_hash(userToLogin.getHashedPassword(), password):
      # The entered password is incorrect.
      return render_template_wrapper('authentication.html', status="The password is incorrect.")

    # If the login is successful, go to main page:
    loggedInID = userToLogin.getId()
    session['userID'] = loggedInID
    return redirect(url_for('index'))

  ### Handle Register Request ###
  @app.route('/auth/register', methods=['POST'])
  def register():
    database = db.Database()
    username = request.form.get("username")
    password = request.form.get("password")

    # Check to see if a user already exists with this username
    possibleUser = database.searchUserByUsername(username)
    if possibleUser is not None:
      return render_template_wrapper('authentication.html', status="An account already exists with this username.")

    # If no user exists, hash the password and create a new user.
    hashedPassword = generate_password_hash(password, method='sha256')
    user = database.createUser(username, hashedPassword)
    session['userID'] = user.getId()
    return redirect(url_for('index'))

  ### Handle Logout Request ###
  @app.route('/auth/logout', methods=['GET'])
  def logout():
    if 'userID' in session:
      session.pop('userID')
    return redirect(url_for('index'))

  ### View Ratings Page ###
  @app.route('/rate', methods=['GET'])
  def viewRatings():
    userID = session.get('userID')
    if userID is None:
      return redirect(url_for('auth'))

    user = db.Database().getUser(int(userID))
    ratings = user.getRatings()

    return render_template_wrapper('ratings.html', ratings=ratings,
                                    actorsNotRated=user.getActorsNotRated(),
                                    directorsNotRated=user.getDirectorsNotRated(),
                                    mediasNotRated=user.getMediasNotRated())

  ### Handle request to add a rating ###
  @app.route('/rate/add', methods=['POST'])
  def addRating():
    userID = session.get('userID')
    if userID is None:
      return redirect(url_for('auth'))

    type = request.json.get("type")
    entity_id = int(request.json.get("entity_id"))
    newRating = int(request.json.get("newRating"))
    if type == 'actor':
      actor = db.Database().getActor(entity_id)
      actor.addRating(int(userID), newRating)
    elif type == 'director':
      director = db.Database().getDirector(entity_id)
      director.addRating(int(userID), newRating)
    elif type == 'media':
      media = db.Database().getMedia(entity_id)
      media.addRating(int(userID), newRating)
    else:
      return "Invalid request!"
    return "200"

  ### Handle request to edit a rating ###
  @app.route('/rate/edit', methods=['POST'])
  def editRating():
    userID = session.get('userID')
    if userID is None:
      return redirect(url_for('auth'))

    type = request.json.get("type")
    entity_id = int(request.json.get("entity_id"))
    newRating = int(request.json.get("newRating"))
    if type == 'actor':
      actor = db.Database().getActor(entity_id)
      actor.updateRating(int(userID), newRating)
    elif type == 'director':
      director = db.Database().getDirector(entity_id)
      director.updateRating(int(userID), newRating)
    elif type == 'media':
      media = db.Database().getMedia(entity_id)
      media.updateRating(int(userID), newRating)
    else:
      return "Invalid request!"
    return "200"

  ### Handle request to delete a rating ###
  @app.route('/rate/delete', methods=['POST'])
  def deleteRating():
    userID = session.get('userID')
    if userID is None:
      return redirect(url_for('auth'))

    type = request.json.get("type")
    entity_id = int(request.json.get("entity_id"))
    if type == 'actor':
      actor = db.Database().getActor(entity_id)
      actor.deleteRating(int(userID))
    elif type == 'director':
      director = db.Database().getDirector(entity_id)
      director.deleteRating(int(userID))
    elif type == 'media':
      media = db.Database().getMedia(entity_id)
      media.deleteRating(int(userID))
    else:
      return "Invalid request!"
    return "200"

  ### Handle request to submit a new genre ###
  @app.route('/addEntity/genre', methods=["POST"])
  def submitGenre():
    userID = session.get('userID')
    if userID is None:
      return redirect(url_for('auth'))

    database = db.Database()
    name = request.form.get("name")
    existingGenreList = database.getGenreByName(name)
    if len(existingGenreList) > 0:
      return redirect(url_for('viewGenres', status=f'The genre "{name}" already exists!'))
    description = request.form.get("description")
    database.createGenre(name, description)
    return redirect(url_for('viewGenres', status=f'Genre "{name}" successfully added!'))

  ### Handle request to submit a new actor ###
  @app.route('/addEntity/actor', methods=["POST"])
  def submitActor():
    userID = session.get('userID')
    if userID is None:
      return redirect(url_for('auth'))

    database = db.Database()
    name = request.form.get("name")
    existingActorList = database.getActorByName(name)
    if len(existingActorList) > 0:
      return redirect(url_for('viewActors'), status=f'The actor "{name}" already exists!')
    sex = request.form.get("sex")
    birthDay = request.form.get("day")
    birthMonth = request.form.get("month")
    birthYear = request.form.get("year")
    birthDate = ''
    if birthYear == "":
      birthDate = "?"
    else:
      try:
        birthDate = datetime.date(year=int(birthYear), month=int(birthMonth), day=int(birthDay))
        birthDate = birthDate.isoformat()
      except ValueError:
        return redirect(url_for('viewActors', status=f'Invalid date of birth!'))
    database.createActor(name, sex, birthDate)
    return redirect(url_for('viewActors', status=f'Actor "{name}" successfully added!'))

  ### Handle request to submit a new director ###
  @app.route('/addEntity/director', methods=["POST"])
  def submitDirector():
    userID = session.get('userID')
    if userID is None:
      return redirect(url_for('auth'))

    database = db.Database()
    name = request.form.get("name")
    existingDirectorList = database.getDirectorByName(name)
    if len(existingDirectorList) > 0:
      return redirect(url_for('viewDirectors', status=f'The director "{name}" already exists!'))
    sex = request.form.get("sex")
    birthDay = request.form.get("day")
    birthMonth = request.form.get("month")
    birthYear = request.form.get("year")
    birthDate = ''
    if birthYear == "":
      birthDate = "?"
    else:
      try:
        birthDate = datetime.date(year=int(birthYear), month=int(birthMonth), day=int(birthDay))
        birthDate = birthDate.isoformat()
      except ValueError:
        return redirect(url_for('viewDirectors', status=f'Invalid date of birth!'))
    database.createDirector(name, sex, birthDate)
    return redirect(url_for('viewDirectors', status=f'Director "{name}" successfully added!'))

  ### Handle request to submit a new streaming service ###
  @app.route('/addEntity/streamingService', methods=["POST"])
  def submitStreamingService():
    userID = session.get('userID')
    if userID is None:
      return redirect(url_for('auth'))

    database = db.Database()
    name = request.form.get("name")
    existingServiceList = database.getStreamingServiceByName(name)
    if len(existingServiceList) > 0:
      return redirect(url_for('viewStreamingServices', status=f'The streaming service "{name}" already exists!'))
    database.createStreamingService(name)
    return redirect(url_for('viewStreamingServices', status=f'Streaming Service "{name}" successfully added!'))

  ### View All Genres ###
  @app.route('/view/genre', methods=["GET"])
  def viewGenres():
    status = request.args.get('status') or ""
    genres = db.Database().getAllGenres()
    return render_template_wrapper('viewGenres.html', genres=genres, status=status)

  ### View All Streaming Services ###
  @app.route('/view/streamingService', methods=["GET"])
  def viewStreamingServices():
    status = request.args.get('status') or ""
    services = db.Database().getAllStreamingServices()
    return render_template_wrapper('viewStreamingServices.html', streamingServices=services, status=status)

  ### View All Actors ###
  @app.route('/view/actor', methods=["GET"])
  def viewActors():
    status = request.args.get('status') or ""
    actors = db.Database().getAllActors()
    return render_template_wrapper('viewActors.html', actors=actors, status=status)

  ### View All Directors ###
  @app.route('/view/director', methods=["GET"])
  def viewDirectors():
    status = request.args.get('status') or ""
    directors = db.Database().getAllDirectors()
    return render_template_wrapper('viewDirectors.html', directors=directors, status=status)

  ### View All Media ###
  @app.route('/view/media', methods=["GET"])
  def viewMedias():
    status = request.args.get('status') or ""
    medias = db.Database().getAllMedias()
    return render_template_wrapper('viewMedias.html', medias=medias, status=status)

  ### View/Edit Certain Genre ###
  @app.route('/view/genre/<genre_id>', methods=["GET", "POST"])
  def viewAndUpdateGenre(genre_id):
    genre = db.Database().getGenre(genre_id)
    if genre is None:
      return redirect(url_for('viewGenres', status="Invalid genre id!"))
    if request.method == "GET":
      return render_template_wrapper('viewGenre.html', genre=genre)
    else:
      userID = session.get('userID')
      if userID is None:
        return redirect(url_for('auth'))
      genre.setName(request.form.get('name'))
      genre.setDescription(request.form.get('description'))
      return redirect(url_for('viewAndUpdateGenre', genre_id=genre_id))

  ### View/Edit Certain Streaming Service ###
  @app.route('/view/streamingService/<ss_id>', methods=["GET", "POST"])
  def viewAndUpdateStreamingService(ss_id):
    service = db.Database().getStreamingService(ss_id)
    if service is None:
      return redirect(url_for('viewStreamingServices', status="Invalid streaming service id!"))
    if request.method == "GET":
      return render_template_wrapper('viewStreamingService.html', service=service)
    else:
      userID = session.get('userID')
      if userID is None:
        return redirect(url_for('auth'))
      service.setName(request.form.get('name'))
      return redirect(url_for('viewAndUpdateStreamingService', ss_id=ss_id))

  ### Delete entity (viewable, etc.) ###
  @app.route("/deleteEntity", methods=["POST"])
  def deleteEntity():
    userID = session.get('userID')
    if userID is None:
      return redirect(url_for('auth'))
    database = db.Database()

    type = request.json.get("type")
    if type == "viewable":
      media = database.getMedia(int(request.json.get("mediaId")))
      service = database.getStreamingService(int(request.json.get("serviceId")))
      if media is None or service is None:
        return redirect(url_for('viewStreamingServices', status="Invalid media or service!"))
      service.makeUnavailable(media)
      return "200"

  ### Wrapper for render_template so that user information is always passed through ###
  def render_template_wrapper(*args, **kwargs):
    userInfo = None
    userID = session.get('userID')
    if userID is not None:
      userInfo = json.dumps(db.Database().getUser(userID).toDict())
    return render_template(*args, userInfo=userInfo, **kwargs)

  app.run(host='0.0.0.0', port='8080', debug=True)

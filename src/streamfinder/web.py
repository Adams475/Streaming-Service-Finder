import os
import json
import datetime
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
  @app.route('/', methods=["GET"])
  def index():
    status = request.args.get('status') or ""
    database = db.Database()
    recentlyAddedMediaRows = database.getRecentlyAddedMediaRows()
    genreStats = database.getGenreStats()
    topMediaRows = database.getHighestRatedMediaRows()
    entityCounts = database.getEntityCounts()

    userID = session.get('userID')
    message = "Anonymous User!" if userID is None else f"{database.getUser(int(userID)).getUsername()}!"
    return render_template_wrapper('index.html', recentlyAddedMediaRows=recentlyAddedMediaRows, status=status,
                                    variable_from_python=message, genreStats=genreStats, entityCounts=entityCounts,
                                    topMediaRows=topMediaRows)

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
    userToLogin = database.getUserByUsername(username)

    if userToLogin is None:
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
    possibleUser = database.getUserByUsername(username)
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
    if birthYear == "" or not birthYear.isnumeric():
      birthDate = "?"
    else:
      try:
        birthDate = datetime.date(year=int(birthYear), month=int(birthMonth), day=int(birthDay))
        birthDate = birthDate.isoformat()
      except ValueError:
        return redirect(url_for('viewActors', status=f'Invalid date of birth!'))
    database.createActor(name, sex, birthDate)
    return redirect(url_for('viewActors', status=f'Actor "{name}" successfully added!'))

  ### Handle request to submit new media ###
  @app.route('/addEntity/media', methods=["POST"])
  def submitMedia():
    userID = session.get('userID')
    if userID is None:
      return redirect(url_for('auth'))

    database = db.Database()
    name = request.form.get("mediaName")
    existingMediaList = database.getMediaByName(name)
    if len(existingMediaList) > 0:
      return redirect(url_for('viewMedias', status=f'The media "{name}" already exists!'))
    year = request.form.get("mediaYear")
    genre = database.getGenre(int(request.form.get("mediaGenre")))
    director = database.getDirector(int(request.form.get("mediaDirector")))
    database.createMedia(name, year, genre, director)
    return redirect(url_for('viewMedias', status=f'Media "{name}" successfully added!'))

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
    if birthYear == "" or not birthYear.isnumeric():
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
    actorTableRows = db.Database().getActorTableRows()
    return render_template_wrapper('viewActors.html', actorTableRows=actorTableRows, status=status)

  ### View All Directors ###
  @app.route('/view/director', methods=["GET"])
  def viewDirectors():
    status = request.args.get('status') or ""
    directorTableRows = db.Database().getDirectorTableRows()
    return render_template_wrapper('viewDirectors.html', directorTableRows=directorTableRows, status=status)

  ### View All Media ###
  @app.route('/view/media', methods=["GET"])
  def viewMedias():
    status = request.args.get('status') or ""
    database = db.Database()
    mediaTableRows = database.getMediaTableRows()
    genres = database.getAllGenres()
    directors = database.getAllDirectors()
    return render_template_wrapper('viewMedias.html', mediaTableRows=mediaTableRows, genres=genres, directors=directors, status=status)

  ### View/Edit Certain Media ###
  @app.route('/view/media/<media_id>', methods=["GET", "POST"])
  def viewAndUpdateMedia(media_id):
    status = request.args.get('status') or ""
    database = db.Database()
    media = database.getMedia(media_id)
    if media is None:
      return redirect(url_for('viewMedias', status="Invalid media id!"))
    if request.method == "GET":
      genres = database.getAllGenres()
      directors = database.getAllDirectors()
      return render_template_wrapper('viewMedia.html', status=status, media=media, genres=genres, directors=directors)
    else:
      userID = session.get('userID')
      if userID is None:
        return redirect(url_for('auth'))
      name = request.form.get("name")
      if name != media.getName():
        existingMediaList = media.database.getMediaByName(name)
        if len(existingMediaList) > 0:
          return redirect(url_for('viewAndUpdateMedia', media_id=media_id, status=f'The media "{name}" already exists! You cannot change its name to that!'))
      media.setName(request.form.get('name'))
      media.setReleaseYear(int(request.form.get('releaseYear')))
      media.setGenre(database.getGenre(int(request.form.get('genre'))))
      media.setDirector(database.getDirector(int(request.form.get('director'))))

      starringActorIds = json.loads(request.form.get('actorIds'))
      starringActors = list(map(lambda x: database.getActor(int(x)), starringActorIds))
      media.setStarredActors(starringActors)

      streamingServiceIds = json.loads(request.form.get('streamingServiceIds'))
      streamingServices = list(map(lambda x: database.getStreamingService(int(x)), streamingServiceIds))
      print(streamingServiceIds, streamingServices)
      media.setAvailableStreamingServices(streamingServices)

      return redirect(url_for('viewAndUpdateMedia', media_id=media_id, status="Media updated successfully!"))

  ### Search Page
  @app.route('/search', methods=["GET", "POST"])
  def search():
      database = db.Database()
      media = None
      actor = None
      director = None
      _id = None
      status = ""
      if request.method == "POST":
          search_string = request.form.get('search')
          _id = database.getMediaByName(search_string)
          if _id != []:
            media = database.getMedia(_id[0].media_id)
            print(type(media))
          if media is None:
              _id = database.getActorByName(search_string)
              if _id != []:
                actor = database.getActor(_id[0].actor_id)
              print(media)
          if (media and actor) is None:
              _id = database.getDirectorByName(search_string)
              if _id != []:
                director = database.getDirector(_id[0].director_id)
              print(director)
      if request.method == "POST" and media is None and actor is None and director is None:
        status = "No results found. Make sure you spell their name correctly!"

      return render_template_wrapper('search.html', media=media, actor=actor, director=director, status=status)


  ### View/Edit Certain Genre ###
  @app.route('/view/genre/<genre_id>', methods=["GET", "POST"])
  def viewAndUpdateGenre(genre_id):
      status = request.args.get('status') or ""
      genre = db.Database().getGenre(genre_id)
      if genre is None:
          return redirect(url_for('viewGenres', status="Invalid genre id!"))
      if request.method == "GET":
          return render_template_wrapper('viewGenre.html', status=status, genre=genre)
      else:
          userID = session.get('userID')
          if userID is None:
              return redirect(url_for('auth'))
          name = request.form.get("name")
          if name != genre.getName():
              existingGenreList = genre.database.getGenreByName(name)
              if len(existingGenreList) > 0:
                  return redirect(url_for('viewAndUpdateGenre', genre_id=genre_id, status=f'The genre "{name}" already exists! You cannot change its name to that!'))
          genre.setName(request.form.get('name'))
          genre.setDescription(request.form.get('description'))
          return redirect(url_for('viewAndUpdateGenre', genre_id=genre_id, status="Genre updated successfully!"))

  ### View/Edit Certain Streaming Service ###
  @app.route('/view/streamingService/<ss_id>', methods=["GET", "POST"])
  def viewAndUpdateStreamingService(ss_id):
      status = request.args.get('status') or ""
      service = db.Database().getStreamingService(ss_id)
      if service is None:
          return redirect(url_for('viewStreamingServices', status="Invalid streaming service id!"))
      if request.method == "GET":
          return render_template_wrapper('viewStreamingService.html', status=status, service=service)
      else:
          userID = session.get('userID')
          if userID is None:
              return redirect(url_for('auth'))
          name = request.form.get("name")
          if name != service.getName():
              existingStreamingServiceList = service.database.getStreamingServiceByName(
                  name)
              if len(existingStreamingServiceList) > 0:
                  return redirect(url_for('viewAndUpdateStreamingService', ss_id=ss_id, status=f'The streaming service "{name}" already exists! You cannot change its name to that!'))
          service.setName(request.form.get('name'))

          availableMediaIds = json.loads(
              request.form.get('availableMediaIds'))
          availableMedias = list(
              map(lambda x: service.database.getMedia(int(x)), availableMediaIds))
          service.setAvailableMedia(availableMedias)

          return redirect(url_for('viewAndUpdateStreamingService', ss_id=ss_id, status="Streaming Service updated successfully!"))

  ### View/Edit Certain Actor ###
  @app.route('/view/actor/<actor_id>', methods=["GET", "POST"])
  def viewAndUpdateActor(actor_id):
      status = request.args.get('status') or ""
      actor = db.Database().getActor(actor_id)
      if actor is None:
          return redirect(url_for('viewActors', status="Invalid actor id!"))
      if request.method == "GET":
          return render_template_wrapper('viewActor.html', status=status, actor=actor)
      else:
          name = request.form.get("name")
          if name != actor.getName():
              existingDirectorList = actor.database.getActorByName(name)
              if len(existingDirectorList) > 0:
                  return redirect(url_for('viewAndUpdateActor', actor_id=actor_id, status=f'The actor "{name}" already exists! You cannot change their name to that!'))
          sex = request.form.get("sex")
          birthDay = request.form.get("day")
          birthMonth = request.form.get("month")
          birthYear = request.form.get("year")
          birthDate = ''
          if birthYear == "" or not birthYear.isnumeric():
              birthDate = "?"
          else:
              try:
                  birthDate = datetime.date(
                      year=int(birthYear), month=int(birthMonth), day=int(birthDay))
                  birthDate = birthDate.isoformat()
              except ValueError:
                  return redirect(url_for('viewAndUpdateActor', actor_id=actor_id, status=f'Invalid date of birth!'))
          actor.setName(name)
          actor.setSex(sex)
          actor.setBirthDate(birthDate)

          starringMediaIds = json.loads(request.form.get('starredMediaIds'))
          starringMedias = list(
              map(lambda x: actor.database.getMedia(int(x)), starringMediaIds))
          actor.setStarredMedias(starringMedias)

          return redirect(url_for('viewAndUpdateActor', actor_id=actor_id, status="Actor updated successfully!"))

  # View/Edit Certain Director
  @app.route('/view/director/<director_id>', methods=["GET", "POST"])
  def viewAndUpdateDirector(director_id):
      status = request.args.get('status') or ""
      director = db.Database().getDirector(director_id)
      if director is None:
          return redirect(url_for('viewDirectors', status="Invalid director id!"))
      if request.method == "GET":
          return render_template_wrapper('viewDirector.html', status=status, director=director)
      else:
          name = request.form.get("name")
          if name != director.getName():
              existingDirectorList = director.database.getDirectorByName(
                  name)
              if len(existingDirectorList) > 0:
                  return redirect(url_for('viewAndUpdateDirector', director_id=director_id, status=f'The director "{name}" already exists! You cannot change their name to that!'))
          sex = request.form.get("sex")
          birthDay = request.form.get("day")
          birthMonth = request.form.get("month")
          birthYear = request.form.get("year")
          birthDate = ''
          if birthYear == "" or not birthYear.isnumeric():
              birthDate = "?"
          else:
              try:
                  birthDate = datetime.date(
                      year=int(birthYear), month=int(birthMonth), day=int(birthDay))
                  birthDate = birthDate.isoformat()
              except ValueError:
                  return redirect(url_for('viewAndUpdateDirector', director_id=director_id, status=f'Invalid date of birth!'))
          director.setName(name)
          director.setSex(sex)
          director.setBirthDate(birthDate)
          return redirect(url_for('viewAndUpdateDirector', director_id=director_id, status="Director updated successfully!"))

  app.run(host='0.0.0.0', port='8080', debug=True)

### Wrapper for render_template so that user information is always passed through ###
def render_template_wrapper(*args, **kwargs):
    userInfo = None
    userID = session.get('userID')
    if userID is not None:
      user = db.Database().getUser(userID)
      userInfo = json.dumps({'user_id': user.user_id, 'username': user.getUsername()})
    return render_template(*args, userInfo=userInfo, **kwargs)

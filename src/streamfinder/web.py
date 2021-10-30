import os, json
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


  ### Example of handling GET request with variable passed through
  @app.route('/exampleGET/<multiplier>', methods=['GET'])
  def exampleGET(multiplier):
    num = request.args.get("number")
    adder = request.args.get("adder")
    return render_template_wrapper('index.html', variable_from_python=f"After multiplying by {multiplier} and adding {adder}, your result is: {int(num) * int(multiplier) + int(adder)}")

  ### Example of handling POST request
  @app.route('/examplePOST', methods=['POST'])
  def examplePOST():
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    return render_template_wrapper('index.html', variable_from_python="Your last name was: " + lastName)

  def render_template_wrapper(*args, **kwargs):
    userInfo = None
    userID = session.get('userID')
    if userID is not None:
      userInfo = json.dumps(db.Database().getUser(userID).toDict())
    return render_template(*args, userInfo=userInfo, **kwargs)

  app.run(host='0.0.0.0', port='8080', debug=True)

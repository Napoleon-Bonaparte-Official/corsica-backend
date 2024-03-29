""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


""" Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along """


# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Vid(db.Model):
    __tablename__ = "videos"
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _description = db.Column(db.String(255), nullable=False)
    _views = db.Column(db.Integer, nullable=False)
    _video = db.Column(db.String(255), unique=False, nullable = False)
    _thumbnail = db.Column(db.String, unique=False)
    _videoID = db.Column(db.Integer, unique=True, nullable=True)
    _userID = db.Column(db.String(255), nullable=False)
    _genre = db.Column(db.String(255), unique=False, nullable=False)
    _likes = db.Column(db.Integer, nullable=False)
    _dislikes = db.Column(db.Integer, nullable=False)
    # Define the Notes schema
    # Constructor of a Notes object, initializes of instance variables within object
        # a name getter method, extracts name from object
    def __init__(self, name, description, views, video, thumbnail, userID, genre=""):
        self._name = name
        self._description = description
        self._views = views
        self._video = video
        self._thumbnail = thumbnail
        self._userID= userID
        self._genre = genre
        self._videoID = None
        self._likes = 0
        self._dislikes = 0

    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def description(self):
        return self._description
    
    # a setter function, allows name to be updated after initial object creation
    @description.setter
    def description(self, description):
        self.description = description
    
    @property
    def views(self):
        return self._views
    
    @views.setter
    def views(self, views):
        self._views = views

    @property 
    def likes(self):
        return self._likes
    
    @likes.setter
    def likes(self, likes):
        self._likes = likes
        
    @property
    def dislikes(self):
        return self._dislikes
    
    @dislikes.setter
    def dislikes(self, dislikes):
        self._dislikes = dislikes    
    
    @property
    def video(self):
        return self._video
    
    @video.setter
    def video(self, video):
        self._video = video
    
    @property
    def thumbnail(self):
        return self._thumbnail
    
    @thumbnail.setter
    def thumbnail(self, thumbnail):
        self._thumbnail = thumbnail

    @property
    def videoID(self):
        return self._videoID
    
    @videoID.setter
    def videoID(self, videoID):
        self._videoID = videoID

    @property
    def userID(self):
        return self._userID
    
    @userID.setter
    def userID(self, userID):
        self._userID = userID
        
    @property
    def genre(self):
        return self._genre
    
    @genre.setter
    def genre(self, genre):
        self._genre = genre

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self, base64_encoded):
        try:
            path = app.config['UPLOAD_FOLDER']
            file_decode = base64.b64decode(base64_encoded)
            db.session.add(self)  # Add prepares to persist the Vid object to the 'videos' table
            db.session.commit()  # Commit the changes to the database

            # After committing, the self.id should be populated with the primary key value generated by the database
            self._videoID = self.id
            self._thumbnail = str(self.id) + str(self._thumbnail)
            output_file_path = os.path.join(path, str(self._thumbnail))
            with open(output_file_path, 'wb') as output_file:
                output_file.write(file_decode)

            # Commit again to ensure the changes to _videoID are saved
            db.session.commit()

            return self
        except IntegrityError:
            db.session.rollback()  # Rollback the session to the previous state
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        try:
            path = app.config['UPLOAD_FOLDER']
            file = os.path.join(path, self._thumbnail)
            file_text = open(file, 'rb')
            file_read = file_text.read()
            file_encode = base64.encodebytes(file_read)
            return {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "views": self.views,
                "video": "http://127.0.0.1:8069/videos/" + self.video,
                "thumbnail": self._thumbnail,
                "base64": str(file_encode),
                "videoID": self.videoID,
                "userID": self.userID,
                "genre": self.genre,
                "likes": self.likes,
                "dislikes": self.dislikes
            }
        except:
            return {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "views": self.views,
                "video": "http://127.0.0.1:8069/videos/" + self.video,
                "thumbnail": "",
                "base64": "",
                "videoID": self.videoID,
                "userID": self.userID,
                "genre": self.genre,
                "likes": self.likes,
                "dislikes": self.dislikes
            }
    def put(self):
        try:
            self._views += 1
            db.session.commit()
            return self
        except:
            return None
    
    def like(self):
        try:
            self._likes += 1
            db.session.commit()
            return self
        except: 
            return None
    
    def dislike(self):
        try:
            self._dislikes += 1
            db.session.commit()
            return self
        except: 
            return None
    
def initVideos():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester records for table"""
        video1 = Vid(
            name='Napoleon Bonaparte Edit 1', 
            description="Napoleon the GOAT, omg I love him he's my glorious KING", 
            thumbnail="napoleonbonaparte.jpg", 
            views=0, 
            video="napoleon-bonaparte.mp4", 
            userID="advikg",
            genre="music"
        )
        video2 = Vid(
            name=' Cisco Kaisen', 
            description="He didn't know his TTL had reached zero.", 
            thumbnail="paul-kaisen.jpg", 
            views=0, 
            video="test.mp4", 
            userID="advikg",
            genre="music"
        )


        # video2 = Vid(
                
        # )
        
        videos = [video1, video2] 
        # videos = []
        # videos = [video1, video2, video3, video4, video5, video6, video7]

        """Builds sample user/note(s) data"""
        vid_id = 0
        for vid in videos:
            try:
                path = app.config['UPLOAD_FOLDER']
                file = os.path.join(path, vid.thumbnail)
                file_text = open(file, 'rb')
                file_read = file_text.read()
                file_encode = base64.encodebytes(file_read)
                vid.create(file_encode)
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {vid.vid}")

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _email = db.Column(db.String(255), unique=True, nullable=False)
    _dob = db.Column(db.Date)
    _role = db.Column(db.String(20), default="User", nullable=False)
    # Define _preferences as an ARRAY of strings
    _preferences = db.Column(db.String(255), nullable=False)


    # Demo purposes
    #

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    # posts = db.relationship("Post", cascade="all, delete", backref="users", lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, uid, email, password="123qwerty", dob=date.today(), role="User", preferences="none"):
        self._name = name  # variables with self prefix become part of the object,
        self._uid = uid
        self.set_password(password)
        self._email = email
        self._dob = dob
        self._role = role
        self._preferences = preferences
        
    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name

    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email
    

    # a getter method, extracts email from object
    @property
    def uid(self):
        return self._uid

    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid

    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid

    @property
    def password(self):
        return (
            self._password[0:10] + "..."
        )  # because of security only show 1st characters

    # update password, this is conventional setter
    def set_password(self, password):
        """Create a hashed password."""
        self._password = generate_password_hash(
            password, "pbkdf2:sha256", salt_length=10
        )

    # check password parameter versus stored/encrypted password
    def is_password(self, password):
        """Check against hashed password."""
        result = check_password_hash(self._password, password)
        return result

    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def dob(self):
        dob_string = self._dob.strftime("%m-%d-%Y")
        return dob_string

    # dob should be have verification for type date
    @dob.setter
    def dob(self, dob):
        self._dob = dob


    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, role):
        self._role = role

    def is_admin(self):
        return self._role == "Admin"
    
    # ... (existing code)

    @property
    def preferences(self):
        return self._preferences
    
    @preferences.setter
    def set_preferences(self, preferences):
        self._preferences = preferences
    
    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            "dob": self.dob,
            # "age": self.age,
            "role": self.role,
            "email": self.email,
            "preferences": self.preferences
            # "post s": [post.read() for post in self.posts]
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", uid="", password=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(password) > 0:
            self.set_password(password)
        db.session.commit()
        return self
    
    def update_email(self, email=""):
        if len(email) >= 5 and "@" in email:
            self.email = email
        db.session.commit()
        print(self.email)
        return self
    
    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()


"""Database Creation and Testing """


# Builds working data for testing
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        u1 = User(
            name="Advik Garg", 
            uid="advikg", 
            email="advik@gmail.com",
            password="password",
            dob=date(2001, 9, 12),
            role="Admin"
        )
        u2 = User(
            name="Aashray Reddy", 
            uid="imreddy", 
            email = "aashray@gmail.com",
            password="password",
            dob=date(1945, 8, 6)
        )
        u3 = User(
            name="Will Cheng",
            uid="wcheng",
            password='password',
            email = "will@gmail.com",
            dob=date(2020, 12, 25)
        )
        u4 = User(
            name="Yeongsu Kim", 
            uid="ykim", 
            password="password",
            email="ykim@gmail.com",
            dob=date(1945, 8, 9),
        )
        users = [u1, u2, u3, u4]
        # print("-------------------------- USERS -----------------------------")
        # print(users)
        """Builds sample user/note(s) data"""
        # i = 0
        for user in users:
            try:
                # print(i)
                # print(user)
                user.create()
            except IntegrityError:
                """fails with bad or duplicate data"""
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.uid}")

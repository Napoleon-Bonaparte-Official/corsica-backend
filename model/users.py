from random import randrange
from datetime import date
import os, base64
import json
#from auth_middleware import token_required
from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import Column, Integer, JSON
class Vid(db.Model):
    '''
    Define all the important columns for the videos
    '''
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
    _accountViewsLikesDislikes = db.Column(MutableDict.as_mutable(JSON))
    '''
    Initial constructor for the class
    This initializes attributes for the videos object which includes:
        - The name of the different videos
        - Description of the different videos
        - Views of each video
        - The video name stored locally
        - Thumbnail image name of the video stored within the instances
        - _videoID to correspond to each video
        - userID to correspond to who uploaded the video
        - Genre of the video for sorting
    '''
    def __init__(self, name, description, views, video, thumbnail, userID, genre="", accountViewsLikesDislikes = {"views": [], "likes": [], "dislikes": []}):
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
        self._accountViewsLikesDislikes = accountViewsLikesDislikes


    '''
    Just a bunch of getter and setters
        - Getters -> Get the object's attributes 
        - Setters -> Update the values for any of the object's attributes
    '''

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def description(self):
        return self._description
    
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

    @property
    def accountViewsLikesDislikes(self):
        return self._accountViewsLikesDislikes
    
    @accountViewsLikesDislikes.setter
    def accountViewsLikesDislikes(self, accountViewsLikesDislikes):
        self._accountViewsLikesDislikes = accountViewsLikesDislikes
    
    def create(self, base64_encoded):

        '''
        Params (Base64_encoded):
            - Base64 encoded of the image
        Adds the base64 image to the upload folder (instance/volumes/uploads) in the following format
            - {id}+{image_name}

        Update the database with:
            - corresponding _videoID as the ID
            - _thumbnail is updated to include the {id}+{image_name}

        '''

        try:
            path = app.config['UPLOAD_FOLDER']
            file_decode = base64.b64decode(base64_encoded)
            db.session.add(self)
            db.session.commit()

            self._videoID = self.id
            self._thumbnail = str(self.id) + str(self._thumbnail)
            output_file_path = os.path.join(path, str(self._thumbnail))
            with open(output_file_path, 'wb') as output_file:
                output_file.write(file_decode)

            db.session.commit()

            return self
        except IntegrityError:
            db.session.rollback()
            return None


    '''
    
    Return a JSON getting the base64 of the thumbnail file 
    Return other important READ data
    '''
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
                "dislikes": self.dislikes,
                "accountViewsLikesDislikes": self.accountViewsLikesDislikes
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
                "dislikes": self.dislikes,
                "accountViewsLikesDislikes": self.accountViewsLikesDislikes
            }
    
    '''
    1)
    Put -> Increases the views by 1, but only if the user hasn't already seen the video
    Like -> Increases the likes by 1, but only if the user hasn't already liked the video
    Dislike -> Increase the dislikes by 1


    2) Commits it to the DB, otherwise if there's an error don't return anything
    '''
    
    def put(self, uid):
        try:
            if uid != "None":
                if uid not in self._accountViewsLikesDislikes["views"]:
                    self._accountViewsLikesDislikes["views"].append(uid)
                    print(" before commit", self._accountViewsLikesDislikes['views'])
                    self._views += 1
                    flag_modified(self, "_accountViewsLikesDislikes")
                    db.session.add(self)
                    db.session.commit()
                    print(" After commit", self._accountViewsLikesDislikes['views'])
                    return self
            else:
                self._views += 1
                db.session.commit()
                return self
        except:
            return None
        
    def like(self, uid):
        try:
            if uid != 'None':
                if uid not in self._accountViewsLikesDislikes["likes"]:
                    self._accountViewsLikesDislikes["likes"].append(uid)
                    self._likes += 1
                    flag_modified(self, "_accountViewsLikesDislikes")
                    db.session.commit()
                    return self
            else:
                return {
                    "error": "You must be authorized to perform this action",
                    "message": "To like a video you must be logged in"
                }, 401
        except: 
            return None
    
    def dislike(self, uid):
        try:
            if uid != 'None':
                if uid not in self._accountViewsLikesDislikes["dislikes"]:
                    self._accountViewsLikesDislikes["dislikes"].append(uid)
                    self._dislikes += 1
                    flag_modified(self, "_accountViewsLikesDislikes")
                    db.session.commit()
                    return self
            else:
                return {
                    "error": "You must be authorized to perform this action",
                    "message": "To dislike a video you must be logged in"
                }, 401
        except: 
            return None
    
def initVideos():
    
    '''
    Pass in the different videos as python objects with the different attributes
    Create database and tables and schema based on the different video objects we have
    '''

    with app.app_context():
        db.create_all()
        video1 = Vid(
            name='Napoleon Bonaparte Edit 1', 
            description="Historical video of Napoleon Bonaparte", 
            thumbnail="napoleonbonaparte.jpg", 
            views=0, 
            video="napoleon-bonaparte.mp4", 
            userID="carrot",
            genre="music"
        )
        video2 = Vid(
            name='Cisco Kaisen', 
            description="He didn't know his TTL had reached zero.", 
            thumbnail="blue.png", 
            views=0, 
            video="test.mp4", 
            userID="carrot",
            genre="music"
        )

        video3 = Vid(
            name = "JJK",
            description = "Gojo Satoru",
            thumbnail="jjk.png",
            views=0,
            video="yes.mp4",
            userID="apple",
            genre="gaming"
        )

        video4 = Vid(
            name = "Angry bird",
            description = "Red Angry Bird talking",
            thumbnail="angrybird.png",
            views=0,
            video="bird.mp4",
            userID='apple',
            genre='educational'
        )
        video5 = Vid(
            name = "Walking around",
            description = "Making my way down town",
            thumbnail="walking.jpeg",
            views=0,
            video="funny-shuban.mp4",
            userID='pineapple',
            genre='gaming'
        )
        video6 = Vid(
            name = "Random Meme 1",
            description = "First of the two memes that are on this website",
            thumbnail = "randocat.jpeg",
            views=0,
            video="meme.mp4",
            userID='pineapple',
            genre="gaming"
        )

        video7 = Vid(
            name = "Random Meme 2",
            description = "Second of the two memes that are on this website",
            thumbnail = "randocat2.jpeg",
            views = 0,
            video="meme2.mp4",
            userID='celery',
            genre = "sports"
        
        )

        video8 = Vid(
            name = "Collegeboard AP Computer Science Principles Video",
            description = "AP Computer Science Principles Video",
            thumbnail = "randocat3.jpeg",
            views = 0,
            video="cb.mp4",
            userID='celery',
            genre = "music"

        )
        
        videos = [video1, video2, video3, video4, video5, video6, video7, video8] 
        likes_dislikes_views = {}

        for vid in videos:
            try:
                path = app.config['UPLOAD_FOLDER']
                file = os.path.join(path, vid.thumbnail)
                file_text = open(file, 'rb')
                file_read = file_text.read()
                file_encode = base64.encodebytes(file_read)
                vid.create(file_encode)

                likes_dislikes_views[vid] = {
                    "likes": "", 
                    "dislikes": "",
                    "views": ""
                }
                print("likes dislikes views", likes_dislikes_views)

            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {vid.vid}")


'''
The following code is an extension of a template that my teacher provided for us the schema changes that I added was:
    - Role
    - Preferences
'''

class User(db.Model):
    '''
    Already provided schema from teacher:
    '''
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _email = db.Column(db.String(255), unique=True, nullable=False)
    _dob = db.Column(db.Date)
    _playlist = db.Column(MutableDict.as_mutable(JSON))


    '''
    Extension that I added
        - The role is useful for admins, admins can perform deletion and creation of different user accounts
        - Preferences - Genre of what the user is interested in 
    '''
    _role = db.Column(db.String(20), default="User", nullable=False)
    _preferences = db.Column(db.String(255), nullable=False)


    
    '''
    constructor of a User object, initializes the instance variables within object (self)
    '''
    def __init__(self, name, uid, email, password="123qwerty", dob=date.today(), role="User", preferences="none", playlist={}):
        self._name = name  # variables with self prefix become part of the object,
        self._uid = uid
        self.set_password(password)
        self._email = email
        self._dob = dob
        self._role = role
        self._preferences = preferences
        self._playlist = playlist
        
    '''
    More setters
    '''

    @property
    def playlist(self):
        return self._playlist
    
    @playlist.setter
    def playlist(self, playlist):
        self._playlist = playlist

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email
    
    @property
    def uid(self):
        return self._uid


    @uid.setter
    def uid(self, uid):
        self._uid = uid

    def is_uid(self, uid):
        return self._uid == uid

    @property
    def password(self):
        return (
            self._password[0:10] + "..."
        )  #
    
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

    @property
    def dob(self):
        dob_string = self._dob.strftime("%m-%d-%Y")
        return dob_string

    @dob.setter
    def dob(self, dob):
        self._dob = dob


    def __str__(self):
        return json.dumps(self.read())

    def create(self):
        try:
            db.session.add(self)  
            db.session.commit() 
            return self
        except IntegrityError:
            db.session.remove()
            return None

    '''
    Roles done by me
    '''
    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, role):
        self._role = role

    def is_admin(self):
        return self._role == "Admin"
    
    '''
    Preferences done by me
    '''
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
            "preferences": self.preferences,
            "playlists": self.playlist
            # "post s": [post.read() for post in self.posts]
        }

    def createPlaylist(self, name):
        self._playlist[name] = []
        flag_modified(self, "_playlist")
        db.session.commit()
        return self

    def updatePlaylist(self, name, videoID):
        self._playlist[name].append(videoID)
        flag_modified(self, "_playlist")
        db.session.commit()
        return self

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

'''
No explicit names just random names and DOBs and passwords
'''
def initUsers():
    with app.app_context():
        db.create_all()
        u1 = User(
            name="mickey mouse", 
            uid="carrot", 
            email="carrot@gmail.com",
            password="password",
            dob=date(1945, 9, 12),
            role="Admin",
            preferences="music",
            playlist={}
        )
        u2 = User(
            name="sonic", 
            uid="apple", 
            email = "apple@gmail.com",
            password="password",
            dob=date(1945, 8, 6),
            playlist={}
        )
        u3 = User(
            name="mario",
            uid="pineapple",
            password='password',
            email = "pineapple@gmail.com",
            dob=date(1945, 12, 25),
            playlist={}
        )
        u4 = User(
            name="kirby", 
            uid="celery", 
            password="password",
            email="celery@gmail.com",
            dob=date(1945, 8, 9),
            playlist = {}
        )
        users = [u1, u2, u3, u4]
        """Builds user data"""
        for user in users:
            try:
                user.create()
            except IntegrityError:
                """fails with bad or duplicate data"""
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.uid}")

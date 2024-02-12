""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

class Video(db.Model):
    count = 0
    __tablename__ = 'videos'  # table title is plural, class title is singular

    # Define the video schema with "vars" from object
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    _title = db.Column(db.String(255), unique=False, nullable=False)
    _description = db.Column(db.String(255), unique=True, nullable=False)
    _poster = db.Column(db.String(255), unique=False, nullable=False)
    _views = db.Column(db.Integer, nullable=False)
    _video = db.Column(db.String(255), unique=True, nullable=False)
    _path = db.Column(db.String(255), unique=False, nullable = False)

    # constructor of a video object, initializes the instance variables within object (self)
    def __init__(self, title, poster, description, vid, path):
        self.id = Video.count
        self._title = title    # variables with self prefix become part of the object, 
        self._description = description
        self._poster = poster
        self._views = 0
        self._video = vid
        self._path = path
        Video.count += 1
    # a title getter method, extracts title from object
    @property 
    def id(self):
        return self.id
    @property
    def title(self):
        return self._title
    
    # a setter function, allows title to be updated after initial object creation
    @title.setter
    def title(self, title):
        self._title = title
    
    # a getter method, extracts email from object
    @property
    def description(self):
        return self._description
    
    # a setter function, allows title to be updated after initial object creation
    @description.setter
    def description(self, description):
        self.description = description
        
    @property
    def poster(self):
        return self._poster
    # check if vid parameter matches user id in object, return boolean
        # a getter method, extracts email from object
    @property
    def video(self):
        return self._video
    
    # a setter function, allows title to be updated after initial object creation
    @video.setter
    def video(self, video):
        self._video = video
        
    # check if vid parameter matches user id in object, return boolean
    def is_Vid(self, video):
        return self.video == video
    
    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, path):
        self._path = path
    
    
    
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a video object from video(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "views": self.views,
            "video": self.video,
            "poster": self.poster,
            "path": self.path
        }

    # CRUD update: updates title, vid, password, tokens
    # returns self
    def update(self, dictionary):
        """only updates values in dictionary with length"""
        for key in dictionary:
            if key == "title":
                self.title = dictionary[key]
            if key == "description":
                self.description = dictionary[key]
            if key == "views":
                self.views = dictionary[key]
            if key == "vid":
                self.vid = dictionary[key]
            if key == "path":
                self.path = dictionary[key]
        db.session.commit()
        return self

    # CRUD delete: remove self
    # return self
    def delete(self):
        video = self
        db.session.delete(self)
        db.session.commit()
        return video


"""Database Creation and Testing """


# Builds working data for testing
def initvideos():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester records for table"""
        
        videos = [
            Video(title='Gojo Honored One', descrption="Throughout the heavens and the earth I alone am the honored one",vid='12345', poster="user", path = "qwerty")
        ]

        """Builds sample user/note(s) data"""
        for video in videos:
            try:
                video.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {video.vid}")
                
                


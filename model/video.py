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
    __tablename__ = 'videos'  # table name is plural, class name is singular

    # Define the video schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _description = db.Column(db.String(255), unique=True, nullable=False)
    _views = db.Column(db.Integer)
    _vid = db.Column(db.String(255), unique=True, nullable=False)
    _path = db.Column(db.String(255), unique=False, nullable = False)

    # constructor of a video object, initializes the instance variables within object (self)
    def __init__(self, name, description, views, vid, path):
        self._name = name    # variables with self prefix become part of the object, 
        self._description = description
        self.views = views
        self._vid = vid

    # a name getter method, extracts name from object
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
        
    # check if vid parameter matches user id in object, return boolean
        # a getter method, extracts email from object
    @property
    def vid(self):
        return self._vid
    
    # a setter function, allows name to be updated after initial object creation
    @vid.setter
    def vid(self, vid):
        self._vid = vid
        
    # check if vid parameter matches user id in object, return boolean
    def is_Vid(self, vid):
        return self._vid == vid
    
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
            "name": self.name,
            "description": self.description,
            "views": self.views,
            "vid": self.vid,
            "path": self.path
        }

    # CRUD update: updates name, vid, password, tokens
    # returns self
    def update(self, dictionary):
        """only updates values in dictionary with length"""
        for key in dictionary:
            if key == "name":
                self.name = dictionary[key]
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
            video(name='Gojo Honored One', vid='azeemK', tokens=45),
        ]

        """Builds sample user/note(s) data"""
        for video in videos:
            try:
                video.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {video.vid}")
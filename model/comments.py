from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    _comment = db.Column(db.String(255))
    _videoID = db.Column(db.Integer)
    _user = db.Column(db.String(255))
    # Define the Notes schema
    # Constructor of a Notes object, initializes of instance variables within object
        # a name getter method, extracts name from object
    def __init__(self, comment, videoID, user):
        self._comment = comment
        self._videoID = videoID
        self._user = user

    def getComment(self):
        return self._comment
    
    def comment(self,comment):
        self._comment = comment
        
    def getVideoID(self):
        return self._videoID
    
    def videoID(self,videoID):
        self._videoID = videoID
        
    def getUser(self):
        return self._user
    
    def user(self, user):
        self._user = user    
    
    def create(self):
        try:
            db.session.add(self) 
            db.session.commit() 
            return self
        except IntegrityError:
            db.session.remove()
            return None
    
    def read(self):
        return {
            "comment": self._comment,
            "videoID": self._videoID,
            "user": self._user
        }

def initComments():
    with app.app_context():
        db.create_all()
        c1 = Comment("Bear", 1, "HELLO")
        c2 = Comment("Camel", 1, "HELLO")
        c3 = Comment("Donkey", 1, "HELLO")
        c4 = Comment("Rabbit", 1, "HELLO")
        c5 = Comment("Dog", 1, "HELLO")
        comments = [c1,c2,c3,c4,c5]
        for comment in comments:
            try:
                comment.create()
            except IntegrityError:
                db.session.remove()
                print("error")

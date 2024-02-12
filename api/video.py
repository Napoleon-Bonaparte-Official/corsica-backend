import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
# from auth_middleware import token_required

from model.videos import Video

video_api = Blueprint('video', __name__, url_prefix='/api/videos')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(video_api)

class VideoAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            title = body.get('title')
            if title is None:
                return {'message': f'Title is missing, or is less than 2 characters'}, 400
            description = body.get('description')
            if description is None:
                return {'message': f'Description is missing, or is less than 2 characters'}, 400
            # look for password and dob
            poster = body.get('poster')
            if poster is None:
                return {'message': f'Poster is missing or in the wrong format'}, 400
            video = body.get('video')
            if video is None:
                return {'message': f'Video is missing or in the wrong format'}, 400
            path = body.get('path')
            if path is None:
                return {'message': f'Path is missing or in the wrong format'}, 400

            ''' #1: Key code block, setup USER OBJECT '''
            vid = Video(title,poster,description,video,path)
            # create user in database
            videoJ = vid.create()
            # success returns json of user
            if videoJ:
                return jsonify(videoJ.read())
            # failure returns error
            return {'message': f'Processed {title}, either a format error or  ID {id} is duplicate'}, 400

        def get(self, id): # Read Method
            videos = Video.query.all()    # read/extract all users from database
            for video in videos:
                if(video.id == id):
                    json_ready = [video.read()]
                    break# prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
        

    class _Update(Resource):
        def post(self):
            body = request.get_json()
            uid = body.get('uid')
            if uid is None:
                return {'message': f'User ID missing'}, 400
            email = body.get('email')
            if email is None or "@" not in email:
                return {'message': f'Email is blank or has an invalid format'}, 400
            user = User.query.filter_by(_uid=uid).first()
            if user:
                try:
                    user.update_email(email)
                    return jsonify(user.read())
                except Exception as e:
                    return {
                        "error": "Something went wrong",
                        "message": str(e)
                    }, 500
        def delete(self):
            body = request.get_json()
            uid = body.get('uid')
            user = User.query.filter_by(_uid=uid).first()
            if user:
                try:
                    user.delete()
                    return {f'{uid} has been deleted'}
                except Exception as e:
                    return {
                        "error": "Something went wrong",
                        "message": str(e)
                    }, 500

    class _Security(Resource):
        def post(self):
            try:
                body = request.get_json()
                if not body:
                    return {
                        "message": "Please provide user details",
                        "data": None,
                        "error": "Bad request"
                    }, 400
                ''' Get Data '''
                uid = body.get('uid')
                if uid is None:
                    return {'message': f'User ID is missing'}, 400
                password = body.get('password')
                
                ''' Find user '''
                user = User.query.filter_by(_uid=uid).first()
                if user is None or not user.is_password(password):
                    return {'message': f"Invalid user id or password"}, 400
                if user:
                    try:
                        token = jwt.encode(
                            {"_uid": user._uid},
                            current_app.config["SECRET_KEY"],
                            algorithm="HS256"
                        )
                        resp = Response("Authentication for %s successful" % (user._uid))
                        resp.set_cookie("jwt", token,
                                max_age=3600,
                                secure=True,
                                httponly=True,
                                path='/',
                                samesite='None'  # This is the key part for cross-site requests

                                # domain="frontend.com"
                                )
                        return resp
                    except Exception as e:
                        return {
                            "error": "Something went wrong",
                            "message": str(e)
                        }, 500
                return {
                    "message": "Error fetching auth token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 404
            except Exception as e:
                return {
                        "message": "Something went wrong!",
                        "error": str(e),
                        "data": None
                }, 500

            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Security, '/authenticate')
    api.add_resource(_Update, '/update')
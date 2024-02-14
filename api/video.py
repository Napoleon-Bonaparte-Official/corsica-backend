import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.users import Vid

video_api = Blueprint('video_api', __name__, url_prefix='/api/video')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(video_api)

class VideoAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def put(self):
            body = request.get_json()
            videoID = int(body.get('videoID'))
            if videoID is None:
                return {'message': f'Video ID is missing'}, 400
            video = Vid.query.filter_by(_videoID=videoID).first()
            if video:
                try:
                    put_req = video.put()
                    return jsonify(video.read())
                except Exception as e:
                    return {
                        "error": "Something went wrong",
                        "message": str(e)
                    }, 500
                
        @token_required
        def post(self, current_user): # Create method
            ''' Read data for json body '''
            if request.is_json:
                body = request.get_json()
                ''' Avoid garbage in, error checking '''
                name = body.get('name')
                if name is None:
                    return {'message': f'name is missing, or is less than 2 characters'}, 400

                description = body.get('description')
                if description is None:
                    return {'message': f'Description is missing, or is less than 2 characters'}, 400

                # look for password and dob
                base64 = body.get('base64')
                if base64 is None:
                    return {'message': f'Thumbnail is missing or in the wrong format'}, 400

                video = body.get('video')
                if video is None:
                    return {'message': f'Video is missing or in the wrong format'}, 400
                
                userID = body.get('uid')
                if userID is None:
                    return {'message': f'userID is missing or in the wrong format'}, 400
                
                thumb_name = body.get('thumbnail')
                if thumb_name is None:
                    return {'message': f'Thumbnail name is missing or in the wrong format'}, 400

                genre = body.get('genre')
                print(genre)
                if thumb_name is None:
                    return {'message': f'Genre  is missing or in the wrong format'}, 400
                
                ''' #1: Key code block, setup USER OBJECT '''
                vid = Vid(name=name, thumbnail=thumb_name,description=description,video=video,userID=userID,views=0,genre=genre)
                # create user in database
                videoJ = vid.create(base64)
                # success returns json of user
                if videoJ:
                    return jsonify(videoJ.read())
                # failure returns error
                return {'message': f'Processed {name}, either a format error or  ID {id} is duplicate'}, 400
            
            else:
                video_file = request.files['video']
                # Check if the file has a filename
                if video_file.filename == '':
                    return 'No selected file', 400

                # Save the video file to the 'videos' directory
                video_userID = os.path.join('videos', video_file.filename)
                video_file.save(video_userID)

        def get(self): # Read Method
            videos = Vid.query.all()    # read/extract all users from database
            json_ready = [video.read() for video in videos]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
        
    class _ReadVID(Resource):
        def get(self, vid):
            video = Vid.query.filter_by(_videoID=vid).first()
            data = video.read()
            return jsonify(data)


    api.add_resource(_CRUD, '/')
    api.add_resource(_ReadVID, '/<int:vid>')
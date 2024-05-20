import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response, make_response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.users import Vid
from model.users import User


video_api = Blueprint('video_api', __name__, url_prefix='/api/video')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(video_api)

class VideoAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def put(self):
            '''
            (Params) Body:
                - Video Type (for likes and dislikes)
                - videoID
            1. Query the Video metadata with the corresponding video ID
            2. If the type is set to 0, then run the PUT function in the model to increase the amount of views
            3. If the type is set to 1, then increase the likes by 1
            4. If the type is set to 2, then increase the dislikes by 1
            '''
            body = request.get_json()
            type = int(body.get('type'))
            videoID = int(body.get('videoID'))
            userID = str(body.get('userID'))
            video = Vid.query.filter_by(_videoID=videoID).first()
            if video:
                if type == 0:
                    try:
                        put_req = video.put(userID)
                        return jsonify(video.read())
                    except Exception as e:
                        return {
                            "error": "Something went wrong",
                            "message": str(e)
                        }, 500
                elif type == 1:
                    try:
                        print(userID)
                        if userID == "None":
                            return {'message': f'You must be logged in to like the video'}, 401
                        put_req = video.like(userID)
                        return jsonify(video.read())
                    except Exception as e:
                        return {
                            "error": "Something went wrong",
                            "message": str(e)
                        }, 500
                elif type == 2:
                    try:
                        if userID == "None":
                            return {'message': f"You must be logged in to dislike the video"}, 401
                        put_req = video.dislike(userID)
                        return jsonify(video.read())
                    except Exception as e:
                        return {
                            "error": "Something went wrong",
                            "message": str(e)
                        }, 500
                
                
        @token_required
        def post(self, current_user): # Create method
            ''' 
            Params: 
                - current_user
            - Body of the JSON
                - base64, description, name, userID, thumbnail name, genre
            
            1. Create a python object based on the paramters 
            2. Create the image with the Create method and ready to go for the video
            3. Once created return the JSON of what the new uploaded JSON looks like              
            '''
            if request.is_json:
                body = request.get_json()
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
        '''
        params:
            - Resource: <int:vid> so it takes any resources at /api/video/<vid>
        
        get method:
            - Queries the Video database to find ALL the data paramters in a jsonified format and returns it:
            EXAMPLE:    
                /api/video/0 - returns:
                (JSON) - 
                {
                    base64,
                    description, 
                    dislikes, 
                    genre,
                    id,
                    likes,
                    name,
                    thumbnail,
                    userID
                    video,
                    videoID,
                    views
                    }
            
        '''

        def get(self, vid):
            video = Vid.query.filter_by(_videoID=vid).first()
            data = video.read()
            return jsonify(data)
        

    class _Recommend(Resource):
        def get(self, uid):
            '''
            1. Find who the user is based on the UID
            2. Find what preference of videos the user likes watching
            3. Query all the different videos
            4. For every video find all video genres matching the user's preference
            5. Show the matching videos based on the MOST views and the MOST like to dislike ratio.
            6. Return the Data as JSON 
            '''
            user = User.query.filter_by(_uid=uid).first()
            if user is None:
                return jsonify({"message": "User not found"}), 404
            
            user_preferences = user.preferences
            # Get all videos
            videos = Vid.query.all()

            # Filter videos based on matching genres
            matching_videos = []
            for video in videos:
                if user_preferences == video.genre:
                    matching_videos.append(video)

            # Calculate like to dislike ratio
            for video in matching_videos:
                if video.dislikes != 0:
                    video.like_to_dislike_ratio = video.likes / video.dislikes
                else:
                    video.like_to_dislike_ratio = video.likes

            sorted_videos = sorted(matching_videos, key=lambda x: x.views, reverse=True)

            # Sort matching videos based on like to dislike ratio
            sorted_videos = sorted(sorted_videos, key=lambda x: x.like_to_dislike_ratio, reverse=True)

            # Sort by highest to lowest views within each ratio group

            # Prepare JSON response
            json_ready = [video.read() for video in sorted_videos]
            return jsonify(json_ready)

    
    api.add_resource(_CRUD, '/')
    api.add_resource(_ReadVID, '/<int:vid>')
    api.add_resource(_Recommend, '/recommend/<string:uid>')
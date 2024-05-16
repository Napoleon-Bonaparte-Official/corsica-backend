import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response, make_response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.comments import Comment
from model.users import Vid


comment_api = Blueprint('comment_api', __name__, url_prefix='/api/comment')
api = Api(comment_api)

class commentAPI:        
    class _CRUD(Resource): 
        def get(self, vid) :
            video = Vid.query.filter_by(_videoID=vid).first()
            comments = Comment.query.all()
            matchingComments = []
            for comment in comments:
                if(comment.getVideoID() == vid):
                    matchingComments.append(comment)
            data = []
            for comment in matchingComments:
                com = {
                    "comment": comment.getComment(),
                    "user": comment.getUser()
                }
                data.append(com)
            return jsonify(data)
        
        
    api.add_resource(_CRUD, '/<int:vid>')

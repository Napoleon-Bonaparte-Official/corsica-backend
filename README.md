# Corsica-backend website
- This is the backend of our website where we've included things such as RESTful APIs and SqlAlchemy in order to store data for our videos, logins, comments, descriptions, and playlists for our videos.

### Files and Directories in this Project

These are some of the key files and directories in this project

README.md: An explanation of the backend website and what it contains.

requirements.txt: This file lists the dependencies required to turn this Python project into a Flask/Python project. It may also include other backend dependencies, such as dependencies for working with a database.

main.py: This Python source file is used to run the project. Running this file starts a Flask web server locally on localhost. During development, this is the file you use to run, test, and debug the backend for corsica.

Dockerfile and docker-compose.yml: These files are used to run and test the project in a Docker container. They allow you to simulate the project’s deployment on a server, such as an AWS EC2 instance. Running these files helps ensure that your tools and dependencies work correctly on different machines.

instances: This directory is the standard location for storing data files that you want to remain on the server. For example, SQLite database files can be stored in this directory. Files stored in this location will persist after a web application restart, everything outside of instances will be recreated at restart.

static: This directory is the standard location for files that you want to be cached by the web server. It is typically used for image files (JPEG, PNG, etc.) or JavaScript files that remain constant during the execution of the web server.

api: This directory contains code that receives and responds to requests from external servers. It serves as the interface between the external world and the logic and code in the rest of the project.

api/users:  These API's are guarded by @token_required, test these using Postman, first you must authenticate <http://127.0.0.1:8069/api/users/authenticate> using raw body JSON {"uid": "carrot", "password": "password"} which will obtain a Cookie. Then you can use the API <http://127.0.0.1:8069/api/users>

api/video: The uploading feature for the video.py is guarded by the @token_required to check who is uploading the video. The get method returns the videos formatted properly, while the put method updates the video's likes, views, and dislikes.

api/comments: Posting method for comments and adding them to the database through the api while the get method allows users to read comments.

model: This directory contains files that implement the backend functionality for many of the files in the api directory. For example, there may be files in the model directory that directly interact with the database.

model/comments.py: Handles the comments and data-relational mapping with objects. 

model/users.py: Handles the users data-relational mapping with objects, additionally also handles the videos table in the sqlite. 



# Flask Portfolio Starter

Use this project to create a Flask Server.

GitHub link: https://github.com/nighthawkcoders/cpt

## Getting Started

> Quick steps that can be used with MacOS, WSL Ubuntu, or Ubuntu; this uses Python 3.9 or later as a prerequisite.

- Open a Terminal, clone the project and then cd into the project area
Install Python and then install Python dependencies for Flask, etc.

```bash
pip install -r requirements.txt
```

- Run from Terminal without VSCode, run each time you change schema

  - Setup database with data
  
  ```bash
    ./migrate.sh
  ```

Run the Python server from the command line

    ```bash
    python main.py
    ```

### Open project in VSCode

- Prepare VSCode and run

  - From Terminal run VSCode

    ```bash
    cd ~/vscode/cpt
    code .
    ```

  - Open Setting: Ctl-Shift P or Cmd-Shift
    - Search Python: Select Interpreter
    - Match interpreter to `which python` from terminal

  - Select main.py and Play button
  - Try the Play button and try to Debug

## Idea

> The purpose of project is to serve APIs.  It is the backend piece of a Full-Stack project.  Review `api` folder in project for endpoints.

### Hacks
> Change the starter code to be your own.

- Change the Bootstrap menu, find places to change Nighthawk information
- Change the Home Page, and dress it up with ideas from your project.
- Add some color and fun through VANTA Visuals (birds, halo, solar, net)
- Show some practical and fun links (hrefs) like Twitter, Git, Youtube
- Build a Sample Page (The table is provided as a guide to Jinja)
- Change the project-specific links page

### Files and Directories in this Project

These are some of the key files and directories in this project

README.md: This file contains instructions for setting up the necessary tools and cloning the project. A README file is a standard component of all properly set-up GitHub projects.

requirements.txt: This file lists the dependencies required to turn this Python project into a Flask/Python project. It may also include other backend dependencies, such as dependencies for working with a database.

main.py: This Python source file is used to run the project. Running this file starts a Flask web server locally on localhost. During development, this is the file you use to run, test, and debug the project.

Dockerfile and docker-compose.yml: These files are used to run and test the project in a Docker container. They allow you to simulate the project’s deployment on a server, such as an AWS EC2 instance. Running these files helps ensure that your tools and dependencies work correctly on different machines.

instances: This directory is the standard location for storing data files that you want to remain on the server. For example, SQLite database files can be stored in this directory. Files stored in this location will persist after a web application restart, everything outside of instances will be recreated at restart.

static: This directory is the standard location for files that you want to be cached by the web server. It is typically used for image files (JPEG, PNG, etc.) or JavaScript files that remain constant during the execution of the web server.

api: This directory contains code that receives and responds to requests from external servers. It serves as the interface between the external world and the logic and code in the rest of the project.

api/users:  These API's are guarded by @token_required, test these using Postman, first you must authenticate http://127.0.0.1:8086/api/users/authenticate using raw body JSON {"uid": "toby", "password": "123toby"} which will obtain a Cookie. Then you can use the API http://127.0.0.1:8086/api/users

api/players: These API's are unguarded. The GET method can be run in the browser http://127.0.0.1:8086/api/players/.   PUT, POST, DELETE methods are supported and can be tested in POSTMAN. 

model: This directory contains files that implement the backend functionality for many of the files in the api directory. For example, there may be files in the model directory that directly interact with the database.

templates: This directory contains files and subdirectories used to support the home and error pages of the website.

templates/layouts/base.html:  This is the Jinja2 template that defines the the head and body requirements for all pages within the site.  This includes navbar.html which provides the menu for the site.

templates/index.html: This is the home page for the site.  It extends base.html and shows the usage of bootstrap cards.

templates/table.html: This is a submenu page and it extends base.html and shows the usage of jQuery data table.

projects: This directory contains files for setting up routes to static HTML pages.

projects/project.py:  This Python file sets up routes to render template files.

projects/templates/bp_projects:  This shows additional Jinja2 formatting such as nested extends and url_for.

.gitignore: This file specifies elements to be excluded from version control. Files are excluded when they are derived and not considered part of the project’s original source. In the VSCode Explorer, you may notice some files appearing dimmed, indicating that they are intentionally excluded from version control based on the rules defined in .gitignore.

### Implementation Summary

#### July 2023

- Update README with File Descriptions (anatomy)
- Add JWT and add security features to the data
- Add migrate.sh to support sqlite schema and data upgrade

#### January 2024

- Make this project a template for a Python backend server.
- Add README entries for migrate.sh usage, database setup and migration
- Add README entries for api/users and api/players

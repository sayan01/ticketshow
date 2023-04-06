#!/bin/env python3
from flask import Flask
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

# import utils
import util

# configure Flask app
import config

# Import Flask-WTF forms classes
from forms import *

# Init DB and declare all db models
from models import *

# Init Flask_Login Manager
import auth

# Init routes
import routes

# Init api
import api

if __name__ == '__main__':
    app.run()

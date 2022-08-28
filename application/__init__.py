from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from config import Config
from flask_mongoengine import MongoEngine
try: 
    from flask_restplus import Api, Resource
except ImportError:
    import werkzeug, flask.scaffold
    werkzeug.cached_property = werkzeug.utils.cached_property
    flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
    from flask_restplus import Api, Resource



api=Api()

app=Flask(__name__)
app.config.from_object(Config)

db=MongoEngine()
db.init_app(app)
api.init_app(app)

from application import routes


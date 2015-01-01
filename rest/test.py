#!/usr/bin/env python

from core import db
from core.api import rep
from core.db import models

from flask import Flask
from flask.ext import restful

from sqlalchemy import create_engine as db_connect
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
api = restful.Api(app)

db_engine = db_connect('sqlite:///test.db')
db_session = sessionmaker(bind=db_engine)

__BASE_URI__ = '/rest'

def uri(path):
    return "{0}/{1}".format(
        __BASE_URI__.rstrip('/'),
        path.lstrip('/')
    )


class User(restful.Resource):

    _user_v1 = rep.user.User_V1(base_uri=__BASE_URI__)

    def __init__(self):
        self.session = db_session()

    def get(self, myid):

        _record = self.session.query(models.User)\
            .filter(models.User.userid == myid).first()

        if _record: return _record
        return {'a':None}

    representations = {
        'application/json' : _user_v1.as_json,
    }

class Role(restful.Resource):
    
    _role_v1 = rep.role.Role_V1(base_uri=__BASE_URI__)

    def __init__(self):
        self.session = db_session()

    def get(self, roleid):
        _record = self.session.query(models.Role)\
            .filter(models.Role.roleid == roleid).first()
        if _record: return _record
        return "Not Found", 404

    representations = {
        'application/json' : _role_v1.as_json,
    }



api.add_resource(User, uri(rep.user.__RESOURCE_URI__))
api.add_resource(Role, uri(rep.role.__RESOURCE_URI__))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

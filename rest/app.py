from flask import Flask
from flask.ext import restful

### Great Example: https://github.com/miguelgrinberg/REST-tutorial/blob/master/rest-server-v2.py

"""
This is a working concept. 

Observations:
    A resource is truely a prospective of an entity. As such 1 entity can have multiple prospecitves. 
        That is to say: An entity can have multiple representations (each is a diffrent type of resource).

    A representation might include representations of another type. it is important that any nesting have a max render depth.

    Identities should not nesasarity be a single value. or even a db serigate at all. perhapse we could generate a hash
    for a entity's key.

Coralary:
    An entity should offer multiple normalized representations of itself as an attribute of the entity.
    Each representation should extend abase class that enforces the JSON+HAL standard.
    a representation should NOT be the flask resource. they are diffrent.

Ideas:
    Could we have the routes auto generate bassed on the available entities and there representations?

    would it be possible to generate the curies documenation from pythons docstrings?

Entity:
    user    userid
            username
            displayName
            emailAddress
            verified
            activated
            isActive
            storageLimit
            storageSize
            notes
            requestedDts
            lastAuthorizedDts
            createdDts
            lastModifiedDts

    role    roleid
            displayName
            description
            mgmtRoleid
            isBuiltIn
            createdDts

    membership  userid
                roleid

Resources:

    users   [user]
    user    userid
            username
            displayName
            emailAddress
            isActive
            storageLimit
            storageSize
            notes
            roles -> rel [ { role } ]
            createdDts
            lastAuthorizedDts

    roles   [role]
    role    roleid
            displayName
            description
            mgmtRoleid -> rel { role }
            members -> rel [ { user } ]
            isBuiltIn
            createdDts
"""

app = Flask(__name__)
api = restful.Api(app)

class RelException(Exception):
    pass


class Resource(restful.Resource):
    """ JSON+HAL compliant Resource """
    def __init__(self, *args, **kwargs):
        super(Resource, self).__init__(*args, **kwargs)
        setattr(self,'__doc_key__', "")
        setattr(self,'__doc_href__',"")
        setattr(self,'__resource_url__',"")
        setattr(self,'__ident__',None)
        setattr(self,'__curies__', {})
        setattr(self,'__links__', {})
        setattr(self,'__embedded__', {})
        

    def add_rel(self, rel, name, **kwargs):

        _link = dict([(k,v) for (k,v) in kwargs.items()])
        _link['href'] = rel.uri
        self.__links__['{0}:{1}'.format(rel.__doc_key__, name)] = _link

        if not rel.__doc_key__ in self.__curies__:
            self.__curies__[rel.__doc_key__] = rel.__doc_href__

    def add_emb(self, member, name):
        _e = self.__embedded__.get(name, [])
        _e.append(member)
        self.__embedded__[name] = _e
        
            
    @property
    def uri(self):
        return self.__resource_url__.format(ident=self.ident)

    @property
    def ident(self):
        return self.__ident__

    @ident.setter
    def ident(self, value):
        self.__ident__ = value

    def render(self, embedded=True):
        _ret = { '_links': { 'self': {'href': self.uri} } }
        
        for _name, _data in self.__links__.items():
            _ret['_links'][_name] = _data

        _curies = []
        for _name, _href in self.__curies__.items():
            _curies.append({'name': _name, 'href': _href, 'templated': True})

        if len(_curies) > 0:
            _ret['_links']['curies'] = _curies

        if hasattr(self, 'fields'):
            for k in self.fields:
                _ret[k] = getattr(self, 'fld_{0}'.format(k))

        _embedded = {}
        if embedded:
            for label, items in self.__embedded__.items():
                for res in items:
                    _key = "{0}:{1}".format(res.__doc_key__,label)
                    _emblist = _embedded.get(_key, [])
                    _emblist.append(res.render(False))
                    _embedded[_key] = _emblist

        if len(_embedded) > 0:
            _ret['_embedded'] = _embedded

        return _ret

    def set_fields(self, **kwargs):
        setattr(self,'fields',set([k for k in kwargs]))
        print(self.fields)
        for (k,v) in kwargs.items():
            print('adding attribute',k,'with value of',v)
            setattr(self,'fld_{0}'.format(k), v)


class Role(Resource):
    def __init__(self, *args, **kwargs):
        super(Role, self).__init__(*args, **kwargs)
        self.__resource_url__ = '/role/{ident}'
        self.__doc_key__ = 'ht'
        self.__doc_href__ = 'http://0xbadc0de.com/docs/{rel}'

    def load(key):
        _r = Role()
        _r.ident = 1234
        _r.set_fields(**{
            'displayName': 'Admin',
            'description': 'Global Admin Group',
            'isBuiltIn': True,
            'createdDts': 1415943306,
        })
        return _r

    def get(self, roleid):
        self.ident = '1234'
        self.set_fields(**{
            'displayName': 'Admin',
            'description': 'Global Admin Group',
            'isBuiltIn': True,
            'createdDts': 1415943306,
        })
        owner = Role.load(1234)
        self.add_rel(owner, "owner", title=owner.fld_displayName)
        member = User.load(1234)
        self.add_emb(member, 'members')
        return self.render()

class User(Resource):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__resource_url__ = '/user/{ident}'
        self.__doc_key__ = 'ht'
        self.__doc_href__ = 'http://0xbadc0de.com/docs/{rel}'

    def load(key):
        _r = User()
        _r.ident = 1234
        _r.set_fields(**{
            'username': 'ian',
            'displayName': 'Ian Laird',
            'emailAddress': 'irlaird@gmail.com',
            'isActive': True,
            'storageLimit': 900,
            'storageSize': 0,
            'notes': None,
            'createdDts': 12345,
            'lastAuthorizedDts': 12345,
        })
        return _r
        
    

class Role_layout(restful.Resource):
    def get(self, roleid):
        return {
            '_links': {
                'self': { 'href': '/rest/role/1234' },
                'curies' : [
                    {
                        'name': 'ht',
                        'href': 'http://0xbadcode.com/docs/role/{rel}',
                        'templated': True,
                    }
                ],
                'ht:owner' : {
                    'title': 'Developers',
                    'href': '/rest/role/1233',
                },
            },
            'displayName': "Admin",
            'description': "Global administrators",
            'isBuiltIn': True,
            'createdDts': 1415943306,
            '_embedded' : {
                'ht:members' : [
                    { 
                        'title':'Ian Laird',
                        'href':'/rest/user/2212',
                    }, {
                        'title':'Desiree Laird',
                        'href':'/rest/user/2213',
                    }
                ]
            }
        }
            

api.add_resource(Role, "/rest/role/<roleid>")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')


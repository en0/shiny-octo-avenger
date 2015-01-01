from flask.ext import restful
from flask import Response
from hashlib import md5
from json import dumps


def compute_etag(dictionary_data, algo=md5):
    return algo(dumps(dictionary_data, sort_keys=True).encode()).hexdigest()
    

class Hypermedia(object):

    def __init__(self, fields, private_fields=None, **kwargs):
        self.__base_uri__ = kwargs.get('base_uri', '/').rstrip('/')
        self.__resource_pattern__ = kwargs.get('resource_pattern', '')
        self.__doc_uri__ = kwargs.get('doc_uri', '')
        self.__doc_key__ = kwargs.get('doc_key', '')
        self.__embedded__ = []
        self.__fields__ = fields
        self.__pfields__ = private_fields if private_fields else []
        self.__links__ = {}
        self.__docs__ = {}

    def add_rel(self, jsonhal_key, jsonhal_rep, **kwargs):
        _key = "{0}:{1}".format(jsonhal_rep.doc_key, jsonhal_key)
        self.__docs__[jsonhal_rep.doc_key] = jsonhal_rep.doc_uri
        kwargs.setdefault('href', jsonhal_rep.uri)
        self.__links__[_key] = kwargs.copy()

    def add_embedded(self, name, rep):
        _key = "{0}:{1}".format(rep.doc_key, name)
        self.__docs__[rep.doc_key] = rep.doc_uri
        _eb = self.__embedded__.append((_key, rep))

    def render(self, depth=1):
        _ret = {
            '_links' : {
                'self': { 'href': self.uri },
            },
        }

        for f,v in self.__links__.items():
            _ret['_links'][f] = v.copy()

        _curies = []
        for f,v in self.__docs__.items():
            _curies.append({
                'name':f,
                'href':v,
                'templated':True
            })

        if len(_curies) > 0:
            _ret['_links']['curies'] = _curies

        if depth > 0:
            _embedded = {}

            for (f,v) in self.__embedded__:
                _eb = _embedded.get(f, [])
                _, __eb = v.render(depth=depth-1)
                _eb.append(__eb)
                _embedded[f] = _eb

            if len(_embedded) > 0:
                _ret['_embedded'] = _embedded

        for f in self.__fields__:
            _ret[f] = getattr(self, f)

        ## Return with etag
        return compute_etag(_ret), _ret

    def load_from_entity(self, entity, depth=None):
        """ Load representation from entity.

        We assume the fields provided map 1 to 1.
        If this is not the case, you will need to override this
        method to provide your own mapping.
        """

        for f in self.__fields__:
            if hasattr(entity, f):
                v = getattr(entity, f)
                try: setattr(self, f, v)
                except AttributeError:
                    print("WARN: Attempted to set {0}. Data descriptor has no setter".format(f))
        

        for f in self.__pfields__:
            if hasattr(entity, f):
                v = getattr(entity, f)
                try: setattr(self, f, v)
                except AttributeError:
                    print("WARN: Attempted to set {0}. Data descriptor has no setter".format(f))

        return self


    def as_json(self, data, code, headers=None):
        if not headers: headers = {}
        headers['ETag'], _body = self.load_from_entity(data).render()
        resp = Response(
            dumps(_body, sort_keys=True), 
            mimetype='application/jsonhal', 
            headers=headers
        )

        resp.status_code = code
        return resp


    @property
    def uri(self):
        _dict_fields = dict([(k, getattr(self,k)) for k in self.__fields__])
        _dict_pfields = dict([(k, getattr(self,k)) for k in self.__pfields__])
        _dict_fields.update(_dict_pfields)
        return self.__base_uri__ + self.__resource_pattern__.format(**_dict_fields)

    @property
    def doc_uri(self):
        return self.__doc_uri__

    @doc_uri.setter
    def doc_uri(self, value):
        self.__doc_uri__ = value

    @property
    def doc_key(self):
        return self.__doc_key__

    @doc_key.setter
    def doc_key(self, value):
        self.__doc_key__ = value

    @property
    def resource_pattern(self):
        return self.__resource_pattern__

    @resource_pattern.setter
    def resource_pattern(self, value):
        self.__resource_pattern__ = value


from core.api import Hypermedia
import core.api

__RESOURCE_URI__ = '/user/<int:myid>'
__RESOURCE_PATTERN__ = '/user/{userid}'

class User_V1(Hypermedia):

    def __init__(self, **kwargs):

        self._userid = None
        self._username = None
        self._displayName = None
        self._emailAddress = None
        self._verified = None
        self._activated = None
        self._isActive = None
        self._storageLimit = None
        self._storageSize = None
        self._notes = None
        self._requestedDts = None
        self._lastAuthorizedDts = None
        self._createdDts = None
        self._lastModifiedDts = None

        _fields = [
            'username', 'displayName',
            'emailAddress', 'verified',
            'activated', 'isActive',
            'storageLimit', 'storageSize',
            'notes', 'requestedDts',
            'lastAuthorizedDts',
        ]

        _pfields=[
            'userid'
        ]

        super(User_V1, self).__init__(
            fields=_fields,
            private_fields=_pfields,
            resource_pattern=__RESOURCE_PATTERN__,
            doc_uri='http://0xbadc0de.com/docs/{rel}',
            doc_key=User_V1.__name__,
            **kwargs
        )


    def load_from_entity(self, entity, depth=1):
        super(User_V1, self).load_from_entity(entity)
        if depth > 0:
            for _role in entity.roles:
                _role_link = core.api.rep.role.Role_V1(base_uri=self.__base_uri__)
                _role_link.load_from_entity(_role, depth-1)
                self.add_rel(_role_link.displayName, _role_link)

        return self

    @property
    def userid(self): 
        return self._userid
    @userid.setter
    def userid(self, value): 
        self._userid = value

    @property
    def username(self):
        return self._username
    @username.setter
    def username(self, value):
        self._username = value

    @property
    def displayName(self):
        return self._displayName
    @displayName.setter
    def displayName(self, value):
        self._displayName = value

    @property
    def emailAddress(self):
        return self._emailAddress
    @emailAddress.setter
    def emailAddress(self, value):
        self._emailAddress = value

    @property
    def verified(self):
        return self._verified
    @verified.setter
    def verified(self, value):
        self._verified = value

    @property
    def activated(self):
        return self._activated
    @activated.setter
    def activated(self, value):
        self._activated = value

    @property
    def isActive(self):
        return self._isActive
    @isActive.setter
    def isActive(self, value):
        self._isActive = value

    @property
    def storageLimit(self):
        return self._storageLimit
    @storageLimit.setter
    def storageLimit(self, value):
        self._storageLimit = value

    @property
    def storageSize(self):
        return self._storageSize
    @storageSize.setter
    def storageSize(self, value):
        self._storageSize = value

    @property
    def notes(self):
        return self._notes
    @notes.setter
    def notes(self, value):
        self._notes = value

    @property
    def requestedDts(self):
        return self._requestedDts
    @requestedDts.setter
    def requestedDts(self, value):
        self._requestedDts = value

    @property
    def lastAuthorizedDts(self):
        return self._lastAuthorizedDts
    @lastAuthorizedDts.setter
    def lastAuthorizedDts(self, value):
        self._lastAuthorizedDts = value

    @property
    def createdDts(self):
        return self._createdDts
    @createdDts.setter
    def createdDts(self, value):
        self._createdDts = value

    @property
    def lastModifiedDts(self):
        return self._lastModifiedDts
    @lastModifiedDts.setter
    def lastModifiedDts(self, value):
        self._lastModifiedDts = value


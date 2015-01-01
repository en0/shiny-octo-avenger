from core.api import Hypermedia
import core.api

__RESOURCE_URI__ = '/role/<int:roleid>'
__RESOURCE_PATTERN__ = '/role/{roleid}'

class Role_V1(Hypermedia):
    def __init__(self, **kwargs):

        self._roleid = None
        self._parentid = None
        self._displayName = None
        self._description = None
        self._isBuiltIn = None
        self._createdDts = None
        self._users = None
        self._children = None

        _fields = [
            'displayName',
            'description',
            'isBuiltIn',
            'createdDts',
        ]

        _pfields = [
            'roleid',
            'parentid',
        ]

        super(Role_V1, self).__init__(
            fields=_fields,
            private_fields=_pfields,
            resource_pattern=__RESOURCE_PATTERN__,
            doc_uri='http://0xbadc0de.com/docs/{rel}',
            doc_key=Role_V1.__name__,
            **kwargs
        )

    def load_from_entity(self, entity, depth=1):
        super(Role_V1, self).load_from_entity(entity)
        if depth > 0:
            for _child in entity.children:
                _child_role = Role_V1(base_uri=self.__base_uri__)
                _child_role.load_from_entity(_child, depth-1)
                self.add_embedded("children", _child_role)

            for _user in entity.users:
                _user_link = core.api.rep.user.User_V1(base_uri=self.__base_uri__)
                _user_link.load_from_entity(_user, depth-1)
                self.add_rel("members", _user_link)
                pass

        return self

    @property
    def roleid(self):
        return self._roleid
    @roleid.setter
    def roleid(self, value):
        self._roleid = value

    @property
    def parentid(self):
        return self._parentid
    @parentid.setter
    def parentid(self, value):
        self._parentid = value

    @property
    def displayName(self):
        return self._displayName
    @displayName.setter
    def displayName(self, value):
        self._displayName = value

    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, value):
        self._description = value

    @property
    def isBuiltIn(self):
        return self._isBuiltIn
    @isBuiltIn.setter
    def isBuiltIn(self, value):
        self._isBuiltIn = value

    @property
    def createdDts(self):
        return self._createdDts
    @createdDts.setter
    def createdDts(self, value):
        self._createdDts = value

    @property
    def users(self):
        return self._users
    @users.setter
    def users(self, value):
        self._users = value

    @property
    def children(self):
        return self._children
    @children.setter
    def children(self, value):
        self._children = value


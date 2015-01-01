from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import sqlalchemy as sa


Base = declarative_base()


Membership = sa.Table('membership', Base.metadata,
    sa.Column('userid', sa.Integer, sa.ForeignKey('user.userid')),
    sa.Column('roleid', sa.Integer, sa.ForeignKey('role.roleid'))
)


class User(Base):

    __tablename__ = 'user'

    userid = sa.Column(sa.Integer, sa.Sequence('userid_seq'), primary_key=True)
    username = sa.Column(sa.String(20))
    displayName = sa.Column(sa.String(50))
    emailAddress = sa.Column(sa.String(255))
    verified = sa.Column(sa.Boolean)
    activated = sa.Column(sa.Boolean)
    isActive = sa.Column(sa.Boolean)
    storageLimit = sa.Column(sa.Integer)
    storageSize = sa.Column(sa.Integer)
    notes = sa.Column(sa.String(255))
    requestedDts = sa.Column(sa.Integer)
    lastAuthorizedDts = sa.Column(sa.Integer)
    createdDts = sa.Column(sa.Integer)
    lastModifiedDts = sa.Column(sa.Integer)

    roles = relationship("Role", secondary=Membership)

    def __repr__(self):
        return "<User(displayName={0}, emailAddress={1}, isActive={2})>".format(
            self.displayName,
            self.emailAddress,
            self.isActive,
        )


class Role(Base):

    __tablename__ = 'role'

    roleid = sa.Column(sa.Integer, sa.Sequence('userid_seq'), primary_key=True)
    parentid = sa.Column(sa.Integer, sa.ForeignKey('role.roleid'))
    displayName = sa.Column(sa.String(50))
    description = sa.Column(sa.String(255))
    isBuiltIn = sa.Column(sa.Boolean)
    createdDts = sa.Column(sa.Integer)

    users = relationship("User", secondary=Membership)
    children = relationship("Role")
    
    def __repr__(self):
        return "<Role(displayName={0}, description={1}, isBuiltIn={2})>".format(
            self.displayName,
            self.description,
            self.isBuiltIn,
        )


if __name__ == '__main__':
    _engine = sa.create_engine('sqlite:///test.db', echo=True)
    db = sessionmaker(bind=_engine)()
    Base.metadata.create_all(_engine)

    _i = User(
        username = 'en0',
        displayName = 'Ian Laird',
        emailAddress = 'irlaird@gmail.com',
        verified = True,
        activated = True,
        isActive = True,
        storageLimit = 4096,
        storageSize = 0,
        notes = None,
        requestedDts = 1416194806,
        lastAuthorizedDts = 1416194806,
        createdDts = 1416194806,
        lastModifiedDts = 1416194806
    )

    _r_dev = Role(
        displayName = "Developer",
        description = "Developer SU Group",
        isBuiltIn = True,
        createdDts =  1416194806,
    ) 

    _r_admin = Role(
        displayName = "Administrator",
        description = "Global Administrator",
        isBuiltIn = True,
        createdDts =  1416194806,
    ) 

    _r_user = Role(
        displayName = "User",
        description = "Genral Users Group",
        isBuiltIn = True,
        createdDts =  1416194806,
    ) 

    _r_CustomGroup = Role(
        displayName = "CustomGroup",
        description = "A custom group to test group ownership",
        isBuiltIn = False,
        createdDts =  1416194806,
    ) 
    _r_dev.children.append(_r_CustomGroup)

    _i.roles.append(_r_dev)
    _i.roles.append(_r_admin)
    _i.roles.append(_r_user)

    db.add(_i)
    db.add(_r_dev)
    db.add(_r_admin)
    db.add(_r_user)
    db.add(_r_CustomGroup)

    db.commit()
    

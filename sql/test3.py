from sqlalchemy import create_engine
from sqlalchemy import Column, MetaData, Table
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapper, sessionmaker

#################################################
class User(object):
    """"""

    #-------------------------------------------
    def __init__(self, name, fullname, password):
        """Constructor"""
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

# create a connection to a sqlite database
# turn echo on to see the auto-generated SQL
engine = create_engine("sqlite:///tutorial.db", echo=True)

# this is used to keep track of tables and their attributes
metadata = MetaData()
users_table = Table('users', metadata,
                    Column('user_id', Integer, primary_key=True),
                    Column('name', String),
                    Column('fullname', String),
                    Column('password', String)
                    )
email_table = Table('email', metadata,
                    Column('email_id', Integer, primary_key=True),
                    Column('email_address', String),
                    Column('user_id', Integer, ForeignKey('users.user_id'))
                    )

# create the table and tell it to create it in the
# database engine that is passed
metadata.create_all(engine)

# create a mapping between the users_table and the User class
mapper(User, users_table)

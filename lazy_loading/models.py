from sqlalchemy.orm import relationship, object_mapper
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from lazy_loading.session import get_session


BASE = declarative_base()

class MyBase(object):
    """Base class for Nova Models."""
    __table_initialized__ = True

    def save(self, session=None):
        """Save this object."""
        if not session:
            session = get_session()
        session.add(self)
        session.flush()

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def __iter__(self):
        self._i = iter(object_mapper(self).columns)
        return self

    def next(self):
        n = self._i.next().name
        return n, getattr(self, n)

    def update(self, values):
        """Make the model object behave like a dict"""
        for k, v in values.iteritems():
            setattr(self, k, v)

    def iteritems(self):
        """Make the model object behave like a dict.

        Includes attributes from joins."""
        local = dict(self)
        joined = dict([(k, v) for k, v in self.__dict__.iteritems()
                      if not k[0] == '_'])
        local.update(joined)
        return local.iteritems()

class Instance(BASE, MyBase):
    """Represents a guest vm."""
    __tablename__ = 'instances'
    injected_files = []

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, unique=True)

class InstanceMetadata(BASE, MyBase):
    """Represents a metadata key/value pair for an instance"""
    __tablename__ = 'instance_metadata'
    id = Column(Integer, primary_key=True)
    key = Column(String(255))
    value = Column(String(255))
    instance_id = Column(Integer, ForeignKey('instances.id'), nullable=False)
    instance = relationship(Instance, backref="metadata",
                            foreign_keys=instance_id,
                            primaryjoin=
                                'InstanceMetadata.instance_id == Instance.id')

def register_models():
    """Register Models and create metadata.

    Called from nova.db.sqlalchemy.__init__ as part of loading the driver,
    it will never need to be called explicitly elsewhere unless the
    connection is lost and needs to be reestablished.
    """
    from sqlalchemy import create_engine
    models = (Instance, InstanceMetadata)
    engine = create_engine('sqlite:///test.db', echo=False)
    for model in models:
        model.metadata.create_all(engine)

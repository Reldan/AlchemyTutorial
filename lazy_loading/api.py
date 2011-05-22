from sqlalchemy.orm import joinedload
from sqlalchemy.orm import joinedload_all
from lazy_loading.session import get_session
import models

def instance_get_all():
    session = get_session()
    return session.query(models.Instance).\
                   options(joinedload_all('metadata')).\
                   all()

def instance_create(values):
    """Create a new Instance record in the database.

    context - request context object
    values - dict containing column values.
    """
    metadata = values.get('metadata')
    metadata_refs = []
    if metadata:
        for k, v in metadata.iteritems():
            metadata_ref = models.InstanceMetadata()
            metadata_ref['key'] = k
            metadata_ref['value'] = v
            metadata_refs.append(metadata_ref)
    values['metadata'] = metadata_refs

    instance_ref = models.Instance()
    instance_ref.update(values)

    session = get_session()
    with session.begin():
        instance_ref.save(session=session)
    return instance_ref
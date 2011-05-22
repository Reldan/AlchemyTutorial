import time
import uuid
import models
import api

def create_instances(count):
    for x in xrange(0, count):
        create_instance()


def create_instance():
    api.instance_create({"name":uuid.uuid4().__str__(),
                         "metadata":{
                             "met1":234,
                             "met2":234,
                             "met3":234,
                             "met4":234,
                             "met5":234,
                             "met6":234,
                             "met7":234
                         }})

#create_instances(100)
def get_instances():
   result = api.instance_get_all()
   print "sleeping"
   time.sleep(10)
   print "sleeped"
   return result

for instance in get_instances():
    metadata = instance['metadata']
    for field in metadata:
        print field["key"]
        print field["value"]
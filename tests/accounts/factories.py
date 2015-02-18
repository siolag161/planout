import factory # factory 

import random
import string

from accounts import models, forms

def random_string(length=10):
    return u''.join(random.choice(string.ascii_letters) for x in xrange(length))

class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.BasicUser
    email = factory.Sequence(lambda n: 'user{0}@test.com'.format(n))
    username = factory.Sequence(lambda n: 'user' + str(n))
    # desc = random_string()

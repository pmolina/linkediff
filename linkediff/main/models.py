from django.db import models
from django.contrib.auth.models import User

class Pool(models.Model):
    owner = models.ForeignKey(User, unique=True)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '"%s" created by %s' % (self.name, self.owner,)
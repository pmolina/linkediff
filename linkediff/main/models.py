from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    oauth_token = models.CharField(max_length=200)
    oauth_secret = models.CharField(max_length=200)


class Pool(models.Model):
    owner = models.ForeignKey(UserProfile, db_index=True)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '"%s" created by %s' % (self.name, self.owner,)

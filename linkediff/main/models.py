from django.db import models

class Pool(models.Model):
    owner = models.EmailField(max_length=75)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '"%s" created by %s' % (self.name, self.owner,)
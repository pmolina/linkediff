# -*- coding: utf-8 -*-

import oauth2 as oauth
import simplejson as json

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    oauth_token = models.CharField(max_length=200)
    oauth_secret = models.CharField(max_length=200)

    def __unicode__(self):
        return '%s' % self.user

    def get_data_from_linkedin(self):
        fields = [
            'id',
            'first-name',
            'last-name',
            'skills',
            'num-recommenders',
            'recommendations-received',
            'certifications',
            'languages',
            'courses',
        ]
        token = oauth.Token(self.oauth_token, self.oauth_secret)
        consumer = oauth.Consumer(settings.LINKEDIN_TOKEN, settings.LINKEDIN_SECRET)
        client = oauth.Client(consumer, token)
        headers = {'x-li-format': 'json'}
        url = "http://api.linkedin.com/v1/people/~:(%s)" % ','.join(fields)
        resp, content = client.request(url, "GET", headers=headers)
        return json.loads(content)

    def get_user_data(self):
        return self.get_data_from_linkedin()  # TODO: this should be persisted in the db!


class Pool(models.Model):
    owner = models.ForeignKey(UserProfile, db_index=True)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(UserProfile, related_name='pools')

    def __unicode__(self):
        return '"%s" created by %s' % (self.name, self.owner,)

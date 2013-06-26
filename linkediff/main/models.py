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
    modified = models.DateTimeField(auto_now=True)

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

    def save_linkedin_data(self):
        """ Persists the data from get_user_data() """
        data = self.get_user_data()
        skills = data['skills']
        self.update_skills(skills)

    def update_skills(self, skills):
        skill_values = skills['values']
        my_skill_names = map( lambda x: x['skill']['name'], skill_values)
        #Look for these skills that already are in the db
        known_skills = Skill.objects.filter(description__in=my_skill_names)
        self.skill_set.add(*known_skills)
        #Those that are new have to be first added and then assigned
        new_skills = set(my_skill_names) - set(known_skills)
        new_object_skills = map(lambda x: Skill(description=x), new_skills)
        for sk in new_object_skills:
            sk.save()
        self.skill_set.add(*new_object_skills)


class Pool(models.Model):
    owner = models.ForeignKey(UserProfile, db_index=True)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(UserProfile, related_name='pools')

    def __unicode__(self):
        return '"%s" created by %s' % (self.name, self.owner,)


class Skill(models.Model):
    description = models.CharField(max_length=200)
    user = models.ManyToManyField(UserProfile)

    def __unicode__(self):
        return r'%s' % self.description

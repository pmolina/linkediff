import oauth2 as oauth
import cgi
import simplejson as json
import datetime
import re

from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from main.models import UserProfile
from main.models import Pool

consumer = oauth.Consumer(settings.LINKEDIN_TOKEN, settings.LINKEDIN_SECRET)
client = oauth.Client(consumer)
request_token_url = 'https://api.linkedin.com/uas/oauth/requestToken'
access_token_url = 'https://api.linkedin.com/uas/oauth/accessToken'
authenticate_url = 'https://www.linkedin.com/uas/oauth/authenticate'

def oauth_login(request):
    # Step 1: get the current hostname and port for the callback
    if request.META['SERVER_PORT'] == 443:
        current_server = "https://" + request.META['HTTP_HOST']
    else:
        current_server = "http://" + request.META['HTTP_HOST']
    oauth_callback = current_server + reverse('oauth_authenticated')
    # Step 2: get a request token from LinkedIn
    resp, content = client.request("%s?oauth_callback=%s" %
        (request_token_url, oauth_callback), "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response from provider.")
    # Step 3: store the request token in a session for later use.
    request.session['request_token'] = dict(cgi.parse_qsl(content))
    # Step 4: redirect the user to the authentication URL.
    url = "%s?oauth_token=%s" % (authenticate_url,
        request.session['request_token']['oauth_token'])
    return HttpResponseRedirect(url)

def home(request):
    return render(request, 'home.html')
    html = "<html><body>"
    token = oauth.Token(request.user.get_profile().oauth_token,request.user.get_profile().oauth_secret)
    client = oauth.Client(consumer,token)
    headers = {'x-li-format':'json'}
    url = "http://api.linkedin.com/v1/people/~:(id,first-name,last-name,headline)"
    resp, content = client.request(url, "GET", headers=headers)
    profile = json.loads(content)
    html += profile['firstName'] + " " + profile['lastName'] + "<br/>" + profile['headline']
    return HttpResponse(html)

@login_required
def oauth_logout(request):
    # Log a user out using Django's logout function and redirect them
    # back to the homepage.
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def my_pools(request):
    user = request.user
    all_pools = user.pool_set.all() 
    return render(request, 'my_pools.html', locals() )

  
def oauth_authenticated(request):
    # Step 1: use the request token in the session to build a new client.
    token = oauth.Token(request.session['request_token']['oauth_token'],
        request.session['request_token']['oauth_token_secret'])
    if 'oauth_verifier' in request.GET:
        token.set_verifier(request.GET['oauth_verifier'])
    client = oauth.Client(consumer, token)
    # Step 2: request the authorized access token from LinkedIn
    resp, content = client.request(access_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response from provider.")
    access_token = dict(cgi.parse_qsl(content))
    headers = {'x-li-format': 'json'}
    url = "http://api.linkedin.com/v1/people/~:(id,first-name,last-name)"
    token = oauth.Token(access_token['oauth_token'],
        access_token['oauth_token_secret'])
    client = oauth.Client(consumer,token)
    resp, content = client.request(url, "GET", headers=headers)
    profile = json.loads(content)    
    # Step 3: lookup the user or create them if they don't exist.
    firstname = profile['firstName']
    lastname = profile['lastName']
    identifier = profile['id']
    try:
        user = User.objects.get(username=identifier)
    except User.DoesNotExist:
        user = User.objects.create_user(identifier,
            '%s@linkedin.com' % identifier,
            access_token['oauth_token_secret'])
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        # Save our permanent token and secret for later.
        userprofile = UserProfile()
        userprofile.user = user
        userprofile.oauth_token = access_token['oauth_token']
        userprofile.oauth_secret = access_token['oauth_token_secret']
        userprofile.save()
    # Authenticate the user and log them in using Django's pre-built
    # functions for these things.
    user = authenticate(username=identifier,
        password=access_token['oauth_token_secret'])
    login(request, user)
    return HttpResponseRedirect(reverse('home'))

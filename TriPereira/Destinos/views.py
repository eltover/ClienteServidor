# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import plotly.offline as opy
import plotly.graph_objs as go
import twitter
import json
import pandas
import pandas as pd
import numpy as np
from sodapy import Socrata

# Create your views here.
@login_required
def home(request):
	user = request.user
	print user
	context = locals()
	template = 'destinos/index.html'
	return render(request, template, context)

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return render_to_response('index.html', {}, RequestContext(request))

def get_data(request):
    template = 'destinos/data.html'
    client = Socrata("www.datos.gov.co", None)

    results = client.get("87tt-fa3a", limit=2000)
    results_df = pd.DataFrame.from_records(results)

      
    context = {
        'results_df': client.get("87tt-fa3a", limit=2000),
        
    }
    return render (request, template, context)

# CONSULTA DE DATOS

def resultdata(request):
    value = request.POST.get('codigo')
    value2 = request.POST.get('codigo2')
    client = Socrata("www.datos.gov.co", None)

    results = client.get("87tt-fa3a", limit=2000)
    #print results
    results_df = pd.DataFrame.from_records(results)

    xresult=[]
    yresult=[]
    
    #SACA CADA UNO DE LOS DATOS PARA LAS GRAFICAS
    for t in range (len(results_df)):
        if (True != pd.isnull (results_df.habitaciones[t])):
            x=(results_df.habitaciones[t])
            xresult.append(pd.to_numeric(x))
        if (True != pd.isnull(results_df.tipo[t])):    
            y=(results_df.tipo[t])
            yresult.append(y)
           
    xresults=sorted(xresult)
    yresults=yresult
    

    context = {
        'codigo': value,        
        'codigo2': value2,
        'results_df': client.get("87tt-fa3a", limit=2000),
        'graph': pd.DataFrame.from_records(results),
        'x': xresults,
        'y': yresults        
    }
    template = 'destinos/resultdata.html'
    return render(request, template, context)


#TWITTER

@login_required
def get_followers(request):
	template = loader.get_template('destinos/followers.html')
	CONSUMER_KEY='M2nC2Z5iHjIINVL19AqRWt4dl'
	CONSUMER_SECRET='saxQkjHJq09QDR8zS3j2IEYq8icJHOHez0bG2GWWwbFgwEkFeI'
	OAUTH_TOKEN='209357515-4Ra6IYU02Wr2FDTmMsdfimTS6qLJqromvCKQ7fUZ'
	OAUTH_TOKEN_SECRET='vEnTrRE7woo2JZX03NnexdpvHJjhOmGpnFyLJWL2CI4vx'

	auth = twitter.oauth.OAuth( OAUTH_TOKEN , OAUTH_TOKEN_SECRET, CONSUMER_KEY , CONSUMER_SECRET )
	twitter_api = twitter.Twitter(auth=auth)
	req = request.user
	search_results = twitter_api.friends.list(screen_name=req, count=20)

	followersCountry = getFollowerCountry(search_results)
	ubicaciones = auxContext(followersCountry)

	followers_screen_name = getScreenName(search_results)
	contexto = crearContexto(twitter_api,followers_screen_name, followersCountry)
	ctx={
        'context': contexto,
        'ubicaciones': json.dumps(followersCountry)
    }
	return HttpResponse(template.render(ctx,request))

def auxContext(followersCountry):
    quest = []

    for item in followersCountry:
        quest.append(followersCountry[item])
    return quest


def getFollowerCountry(search_results):
    quest = {}
    i = 0
    aux = ''
    auxname = ''
    while  i < len(search_results['users']):
        quest[search_results['users'][i]['screen_name']] = search_results['users'][i]['location']
        i += 1
    return quest



def getScreenName(followers):
    quest = []
    i = 0
    while i < len(followers['users']):
        quest.append(followers['users'][i]['screen_name'])
        i += 1
    return quest

def crearContexto(twitter_api, followers, countries):
    quest = {}
    followers_last_tweet = []
    aux = []
    coordinates = []

    for name in followers:
        followers_last_tweet = twitter_api.statuses.user_timeline(screen_name=name, count=1)
        try:
            coordinates = followers_last_tweet[0]['geo']['coordinates']
        except:
            coordinates = []

        aux = [ followers_last_tweet[0]['text'], coordinates, countries[name] ]
        quest[name] = aux

    return quest

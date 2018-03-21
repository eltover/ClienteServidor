# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import HttpResponse


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



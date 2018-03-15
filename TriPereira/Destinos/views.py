# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import HttpResponse


# Create your views here.
def home(request):
	context = locals()
	template = 'destinos/index.html'
	return render(request, template, context)

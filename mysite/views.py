from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext

from .helpers import *

class Home(View):
	def get(self, request):
		cart_len = cart_count(request)
		response = render(request, 'home.html', {'cart_len': cart_len})
		response.set_cookie('uid', 'somethingunique')
		return response
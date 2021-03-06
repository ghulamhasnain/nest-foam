from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext

from .models import Subcategory as Subcat
from .models import Category as Cat
from .helpers import *

# Create your views here.

class Category(View):
	def get(self, request, category):

		cart_len = cart_count(request)

		categoryName = unslugify(category)
		category = Cat.objects.get(name = categoryName)
		subcategories = Subcat.objects.filter(category = category)

		if subcategories.count() > 0:
			return render(request, 'subcategories.html', {'category': category, 'subcategories': subcategories, 'cart_len': cart_len})

		else:
			return HttpResponse('ok')

class Subcategory(View):
	def get(self, request, category, subcategory):

		cart_len = cart_count(request)
		
		if subcategory == 'sofa':
			return render(request, 'sofa.html', {'cart_len': cart_len})
		elif subcategory == 'floor':
			return render(request, 'floor.html', {'cart_len': cart_len})
		elif subcategory == 'dining-chair':
			return render(request, 'dining-chair.html', {'cart_len': cart_len})
		elif subcategory == 'mattress':
			return render(request, 'mattress.html', {'cart_len': cart_len})
		elif subcategory == 'topper':
			return render(request, 'topper.html', {'cart_len': cart_len})
		elif subcategory == 'packaging':
			return render(request, 'packaging.html', {'cart_len': cart_len})
		elif subcategory == 'sound-proofing':
			return render(request, 'sound-proofing.html', {'cart_len': cart_len})
		elif subcategory == 'craft':
			return render(request, 'craft.html', {'cart_len': cart_len})

		else:
			return HttpResponse('subcat page')

	def post(self, request, category, subcategory):

		foamType = request.POST.get('type')
		length = float(request.POST.get('length'))
		width = float(request.POST.get('width'))
		height = float(request.POST.get('height'))
		material = request.POST.get('material')
		colour = request.POST.get('colour')
		quantity = int(request.POST.get('quantity'))

		if foamType != 'dining-chair':

			if length > 0 and width > 0 and height > 0:
				area = length * width * height
			else:
				area = 0


			if material in materials and colour in colours:
				unit_price = area * pricing[category][subcategory][foamType][material][colour]
				price = unit_price * quantity

			else:
				price = 0

			if price > 0:

				session_value = [category, subcategory, foamType, length, width, height, material, colour, quantity, roundToTwoDecimalPlaces(price), roundToTwoDecimalPlaces(unit_price)]

				try:
					session = request.session['cart']
					session.append(session_value)
					request.session['cart'] = session
				
				except:
					request.session['cart'] = [session_value]

				return redirect('/products/'+category+'/'+subcategory)

			else:
				return HttpResponse('not sessioned')

		else:
			
			if colour == "custom":

				if length > 0 and width > 0 and height > 0:
					area = length * width * height
				else:
					area = 0


				if material in materials and colour in colours:
					unit_price = area * pricing[category][subcategory][foamType][material][colour]
					price = unit_price * quantity

				else:
					price = 0

			else:

				try:
					unit_price = pricing[category][subcategory][foamType][material][colour]
					price = unit_price * quantity
				except Exception as e:
					price =  0

			if price > 0:

				session_value = [category, subcategory, foamType, length, width, height, material, colour, quantity, roundToTwoDecimalPlaces(price), roundToTwoDecimalPlaces(unit_price)]

				try:
					session = request.session['cart']
					session.append(session_value)
					request.session['cart'] = session
				
				except:
					request.session['cart'] = [session_value]

				return redirect('/products/'+category+'/'+subcategory)

			else:
				return HttpResponse('not sessioned')

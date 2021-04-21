from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext

from .models import Subcategory as Subcat
from .models import Category as Cat
from .helpers import *

# Create your views here.

class Home(View):
	def get(self, request):
		categories = Cat.objects.all()

		cart_len = cart_count(request)

		response = render(request, 'home.html', {'categories': categories, 'cart_len': cart_len})

		response.set_cookie('uid', 'somethingunique')

		return response

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
				price = area * pricing[category][subcategory][foamType][material][colour] * quantity

			else:
				price = 0

			if price > 0:

				session_value = [category, subcategory, foamType, length, width, height, material, colour, quantity, roundToTwoDecimalPlaces(price)]

				try:
					session = request.session['cart']
					session.append(session_value)
					request.session['cart'] = session
				
				except:
					request.session['cart'] = [session_value]

				return redirect('/'+category+'/'+subcategory)

			else:
				return HttpResponse('not sessioned')

		else:
			
			if colour == "custom":

				if length > 0 and width > 0 and height > 0:
					area = length * width * height
				else:
					area = 0


				if material in materials and colour in colours:
					price = area * pricing[category][subcategory][foamType][material][colour] * quantity

				else:
					price = 0

			else:

				try:
					price = pricing[category][subcategory][foamType][material][colour] * quantity
				except Exception as e:
					price =  0

			if price > 0:

				session_value = [category, subcategory, foamType, length, width, height, material, colour, quantity, roundToTwoDecimalPlaces(price)]

				try:
					session = request.session['cart']
					session.append(session_value)
					request.session['cart'] = session
				
				except:
					request.session['cart'] = [session_value]

				return redirect('/'+category+'/'+subcategory)

			else:
				return HttpResponse('not sessioned')


class Cart(View):
	def get(self, request):

		cart_len = cart_count(request)

		try:
			cart = request.session['cart']

		except:
			cart = []

		cart_total = 0

		if cart_len > 0:
			for c in cart:
				cart_total = cart_total + c[-1]

		return render(request, 'cart.html', {'cart_len': cart_len, 'cart': cart, 'cart_total': roundToTwoDecimalPlaces(cart_total)})

class DeleteCartEntry(View):
	def get(self, request, linenum):

		cart_len = cart_count(request)
		cart = request.session['cart']
		line_to_delete = cart[linenum-1]
		del cart[linenum-1]

		request.session['cart'] = cart

		return redirect('cart')

class EmptyCart(View):
	def get(self, request):

		request.session['cart'] = ''

		return redirect('cart')
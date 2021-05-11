import json

from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.template import RequestContext

from .models import *
from .helpers import *
from orders.models import *
from products.models import *
from products.helpers import *

# Create your views here.
class Cart(View):
	def get(self, request):
		cart_len = cart_count(request)
		try:
			cart = request.session['cart']
		except:
			cart = []

		cart_total = getCartTotal(request)

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

class PaymentComplete(View):
	def get(self, request):
		cart = getCartContents(request)
		return HttpResponse(cart)

	def post(self, request):
		from paypalcheckoutsdk.orders import OrdersGetRequest
		from .paypalinit import PayPalClient

		PPClient = PayPalClient()

		body = json.loads(request.body)
		data = body["orderID"]

		requestorder = OrdersGetRequest(data)
		response = PPClient.client.execute(requestorder)

		total_paid = response.result.purchase_units[0].amount.value

		cart = getCartContents(request)

		order = Order.objects.create(
			email = response.result.payer.email_address,
			full_name = response.result.purchase_units[0].shipping.name.full_name,
			address1 = response.result.purchase_units[0].shipping.address.address_line_1,
			address2 = response.result.purchase_units[0].shipping.address.admin_area_2,
			postal_code = response.result.purchase_units[0].shipping.address.postal_code,
			country_code = response.result.purchase_units[0].shipping.address.country_code,
			total_paid = response.result.purchase_units[0].amount.value,
			order_key = response.result.id,
			payment_option = "paypal",
			billing_status = True,
		)

		order_id = order.pk

		for item in cart:
			category = Category.objects.get(name = unslugify(item[0]))
			subcategory = Subcategory.objects.get(name = unslugify(item[1]))

			OrderItem.objects.create(order_id = order_id, category_id = category.pk, subcategory_id = subcategory.pk, item_type = item[2], length = item[3], width = item[4], height = item[5], material = item[6], colour = item[7], quantity = item[8])
			return JsonResponse("Payment Complete!!!", safe=False)

class PaymentSuccessful(View):
	def get(self, request):
		request.session['cart'] = ''
		return HttpResponse('Payment successful')

class Payment(View):
	def get(self, request):
		cart_total = str(getCartTotal(request))
		cart_total = cart_total.replace(".", "")
		cart_total = int(cart_total)

		stripe.api_key = "pk_test_51InWoRCzModAlN49GTx8sTTobO6TIIX5Re6Uuadzq6QuyQaCFzxcKqQUnJqJpqvSJyKo37BQ4dzhLmGk1Fi8P8Jj00RevkBmaG"
		intent = stripe.PaymentIntent.create(
			amount = cart_total,
			currency = 'gbp'
		)
		return render(request, 'payment.html', {'client_secret': intent.client_secret})
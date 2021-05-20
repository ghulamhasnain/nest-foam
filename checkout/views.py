import json

from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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

		return redirect('/cart')

class EmptyCart(View):
	def get(self, request):
		request.session['cart'] = ''
		return redirect('/cart')

class PaypalPaymentComplete(View):
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
			OrderItem.objects.create(order_id = order_id, category_id = category.pk, subcategory_id = subcategory.pk, item_type = item[2], length = float(item[3]), width = float(item[4]), height = float(item[5]), material = item[6], colour = item[7], quantity = int(item[8]))
			return JsonResponse("Payment Complete!!!", safe=False)

class PaymentSuccessful(View):
	def get(self, request):
		request.session['cart'] = ''
		return HttpResponse('Payment successful')

@method_decorator(csrf_exempt, name='dispatch')
class CheckoutStripe(View):
	def get(self, request):
		import stripe
		stripe.api_key = secret_key

		## prepare line_items
		cart = request.session['cart']
		line_items = []

		for item in cart:
			name = item[1] if item[1] == item[2] else item[1] + ' (' + item[2] + ')'
			size = str(item[3]) + ' x ' + str(item[4]) + ' x ' + str(item[5])
			if item[1] == 'dining-chair' or item[1] == 'floor':
				material = item[6]
			else:
				material = item[6] + ' (' + item[7] + ')'
			quantity = int(item[8])
			per_unit_amount = roundtoTwoDecimalPlacesWithoutDecimal(item[9] / quantity)

			line_items.append(
				{
					'price_data': {
						'currency': 'gbp',
						'product_data': {
							'name': name,
							'description': material + ' ' + size,
						},
						'unit_amount': per_unit_amount,
					},
					'quantity': quantity,
				}
			)

		## create stripe checkout session
		session = stripe.checkout.Session.create(
			payment_method_types=['card'],
			line_items=line_items,
			mode='payment',
			success_url='http://ghulamhasnain.pythonanywhere.com/cart/checkout/complete',
			cancel_url='http://ghulamhasnain.pythonanywhere.com/cart/checkout/cancel',
		)

		return JsonResponse({
			'session_id' : session.id,
			'stripe_public_key' : public_key
		})

class StripePaymentComplete(View):
	def get(self, request):
		cart = getCartContents(request)

		order = Order.objects.create(
			email = "response.result.payer.email_address",
			full_name = "response.result.purchase_units[0].shipping.name.full_name",
			address1 = "response.result.purchase_units[0].shipping.address.address_line_1",
			address2 = "response.result.purchase_units[0].shipping.address.admin_area_2",
			postal_code = "KDKDKDK",
			country_code = "GB",
			total_paid = getCartTotal(request),
			payment_option = "stripe",
			billing_status = True,
		)

		order_id = order.pk

		for item in cart:
			category = Category.objects.get(name = unslugify(item[0]))
			subcategory = Subcategory.objects.get(name = unslugify(item[1]))
			try:
				OrderItem.objects.create(order_id = order_id, category_id = category.pk, subcategory_id = subcategory.pk, item_type = item[2], length = float(item[3]), width = float(item[4]), height = float(item[5]), material = item[6], colour = item[7], quantity = int(item[8]))
				return redirect("/cart/payment_successful")
			except:
				return HttpResponse("order not created in db")

class CheckoutCancel(View):
	def get(self, request):
		return HttpResponse('cancel')

@method_decorator(csrf_exempt, name='dispatch')
class Checkout(View):
	def get(self, request):
		cart_total = str(getCartTotal(request))

		return render(request, "checkout.html", {"public_key": public_key, "cart_total": cart_total})
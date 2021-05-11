def cart_count(request):
	try:
		cart = request.session['cart']
		cart_len = len(cart)
	except:
		cart_len = 0
	return cart_len

def roundToTwoDecimalPlaces(number):
	return float("{:.2f}".format(number))

def getCartContents(request):
	try:
		cart = request.session['cart']

	except:
		cart = []

	return cart

def getCartTotal(request):
	cart_len = cart_count(request)

	try:
		cart = request.session['cart']
	except:
		cart = []
	
	cart_total = 0
	if cart_len > 0:
		for c in cart:
			cart_total = cart_total + c[-1]

	return cart_total
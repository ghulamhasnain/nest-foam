def cart_count(request):
	try:
		cart = request.session['cart']
		cart_len = len(cart)
	except:
		cart_len = 0
	return cart_len

def roundToTwoDecimalPlaces(number):
	return float("{:.2f}".format(number))

def roundtoTwoDecimalPlacesWithoutDecimal(number):
	num = roundToTwoDecimalPlaces(number)
	num = format(num, '.2f')
	num = num.replace('.', '')
	num = int(num)
	return num

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
			cart_total = cart_total + c[-2]

	return cart_total

public_key = "pk_test_51InWoRCzModAlN49GTx8sTTobO6TIIX5Re6Uuadzq6QuyQaCFzxcKqQUnJqJpqvSJyKo37BQ4dzhLmGk1Fi8P8Jj00RevkBmaG"

secret_key = "sk_test_51InWoRCzModAlN49mDMevVeGKNECHDDpQqKvOa62Y6d4PlYnOu3hipq688M3OvycoImgepdyMLRusujldK5FMwxK00YchhglyD"
def cart_count(request):
	try:
		cart = request.session['cart']
		cart_len = len(cart)

	except:
		cart_len = 0

	return cart_len
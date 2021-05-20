console.log('ok')

var checkoutButton = document.querySelector("#checkout-button");

checkoutButton.addEventListener('click', function(event) {   
	fetch('/cart/checkout_stripe')
	.then((result) => { 
		return result.json()
	})
	.then((data) => {
		var stripe = Stripe(data.stripe_public_key);
		stripe.redirectToCheckout({
		// Make the id field from the Checkout Session creation API response
		// available to this file, so you can provide it as parameter here
		// instead of the {{CHECKOUT_SESSION_ID}} placeholder.
			sessionId: data.session_id
		}).then(function (result) {
		// If `redirectToCheckout` fails due to a browser or network
		// error, display the localized error message to your customer
		// using `result.error.message`.
		});
	}) 
})
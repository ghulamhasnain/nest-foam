"""foamsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path

from . import views

urlpatterns = [
	path('', views.Cart.as_view(), name='cart'),
    path('delete/<int:linenum>', views.DeleteCartEntry.as_view(), name='deletecartentry'),
    path('empty', views.EmptyCart.as_view(), name='empty'),
    
    path('payment_complete', views.PaypalPaymentComplete.as_view(), name="payment_complete"), ##Paypal payment complete
    path('payment_successful', views.PaymentSuccessful.as_view(), name="payment_successful"), #Paypal payment successful

    path('checkout', views.Checkout.as_view(), name='checkout'),
    path('checkout_stripe', views.CheckoutStripe.as_view(), name='checkout_stripe'),
    path('checkout/complete', views.StripePaymentComplete.as_view(), name='success'),
    path('checkout/cancel', views.CheckoutCancel.as_view(), name='cancel')
]
from django.db import models

from products.models import *

# Create your models here.
class Order(models.Model):
	email = models.CharField(max_length=50)
	full_name = models.CharField(max_length=50)
	address1 = models.CharField(max_length=250)
	address2 = models.CharField(max_length=250)
	city = models.CharField(max_length=100)
	phone = models.CharField(max_length=50)
	postal_code = models.CharField(max_length=50)
	country_code = models.CharField(max_length=50)
	total_paid = models.DecimalField(max_digits=5, decimal_places=2)
	order_key = models.CharField(max_length=50, default="")
	billing_status = models.BooleanField(default=False)
	payment_option = models.CharField(max_length=50)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.created)

class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name="orderitems", on_delete=models.CASCADE)
	category = models.ForeignKey(Category, related_name="ordercategory", on_delete=models.CASCADE)
	subcategory = models.ForeignKey(Subcategory, related_name="ordersubcategory", on_delete=models.CASCADE)
	item_type = models.CharField(max_length=50)
	length = models.FloatField(default=1)
	width = models.FloatField(default=1)
	height = models.FloatField(default=1)
	material = models.CharField(max_length=50)
	colour = models.CharField(max_length=50)
	quantity = models.IntegerField(default=1)

	def __str__(self):
		return str(self.id)
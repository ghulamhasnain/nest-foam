from django.db import models

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=24, unique=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Subcategory(models.Model):
	name = models.CharField(max_length=24, unique=True)
	category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='subcategory_category', null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class CartItems(models.Model):
	uid = models.CharField(max_length=24, unique=False)
	category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='cart_items_category', null=False, blank=False)
	subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, related_name='cart_items_subcategory', null=False, blank=False)
	size = models.CharField(max_length=24, default = '')
	material = models.CharField(max_length=24, default = '')
	quantity = models.IntegerField(default = 1)
	price = models.DecimalField(default = 1.0, max_digits = 10, decimal_places = 2)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.uid
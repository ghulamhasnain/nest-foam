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
from django.db import models
from data.models import *
from api.translator import Translator
from datetime import date


t = Translator()

class Company(models.Model):
	documentIdentification = models.TextField(unique = True)
	type_documentI = models.ForeignKey(Type_Document_Identification,on_delete = models.CASCADE)
	type_organization = models.ForeignKey(Type_Organization,on_delete=models.CASCADE)
	type_regime = models.ForeignKey(Type_Regime,on_delete=models.CASCADE)
	business_name = models.TextField()
	municipality = models.ForeignKey(Municipality,on_delete=models.CASCADE)
	address = models.TextField()
	phone = models.TextField()
	email = models.TextField()
	certificate_generation_date = models.CharField(max_length=10)
	certificate_expiration_date = models.CharField(max_length=10)
	resolution_generation_date = models.CharField(max_length=10)
	resolution_expiration_date = models.CharField(max_length=10)
	block = models.BooleanField(default = False)
	token = models.TextField()
	user = models.TextField()
	password = models.TextField()
	logo = models.ImageField(upload_to = "Logo_Company",default = "Logo_Company/default.png")
	cod_bars = models.BooleanField(default = True)
	resolution_number = models.TextField(default = "18760000001")
	prefix = models.TextField(default = "SETP")
	license = models.BooleanField(default = False)
	date_register = models.TextField(default=date.today())
	payment_date = models.TextField(default = date.today())

	def __str__(self):
		name = t.decodificar(self.business_name)
		return name




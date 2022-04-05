from django.db import models
from api.translator import Translator
from client.models import Client
from company.models import Company
from data.models import *
t = Translator()

class POS(models.Model):
	number = models.TextField()
	prefix = models.TextField()
	code = models.TextField()
	quanty = models.TextField()
	description = models.TextField()
	price = models.TextField()
	tax = models.TextField()
	notes = models.TextField()
	date = models.TextField()
	ipo = models.TextField()
	discount = models.TextField()
	client = models.ForeignKey(Client,on_delete = models.CASCADE)
	company = models.ForeignKey(Company,on_delete = models.CASCADE)
	type = models.TextField(default = "FE")#FE - POS

	def Base_Product(self):
		return ( float(t.decodificar(self.price)) - float(t.decodificar(self.ipo)) ) / (1 + (float(t.decodificar(self.tax)) / 100) )

	def Tax_Value(self):
		return ( float(t.decodificar(self.price)) - self.Base_Product() )

	def Base_Product_WithOut_Discount(self):
		return self.Base_Product() - ( float(t.decodificar(self.discount)) * 100 )

	def Totals(self):
		return (self.Base_Product_WithOut_Discount() + self.Tax_Value() + float(t.decodificar(self.ipo))) * float(t.decodificar(self.quanty))


class Payment_Form_Invoice_POS(models.Model):
	payment_form_id = models.ForeignKey(Payment_Form,on_delete=models.CASCADE)
	payment_method_id = models.ForeignKey(Payment_Method,on_delete=models.CASCADE)
	payment_due_date = models.TextField()
	duration_measure = models.TextField()
	pos = models.ForeignKey(POS,on_delete=models.CASCADE)


class Wallet_POS(models.Model):
	pos = models.ForeignKey(POS,on_delete=models.CASCADE)
	client = models.ForeignKey(Client,on_delete = models.CASCADE)
	price = models.TextField()
	date = models.TextField()

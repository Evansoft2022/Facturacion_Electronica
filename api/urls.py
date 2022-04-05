from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^Create_Company$',Create_Company,name="Create_Company"),
		url(r'^Create_Client$',Create_Client,name="Create_Client"),
		url(r'^Create_Invoice_$',Create_Invoice_,name="Create_Invoice_"),
		url(r'^Create_Payroll$',Create_Payroll,name="Create_Payroll"),
		url(r'^Create_Category$',Create_Category,name="Create_Category"),
		url(r'^Create_Inventory$',Create_Inventory,name="Create_Inventory"),
		url(r'^Create_Empleoyee$',Create_Empleoyee,name="Create_Empleoyee"),
		url(r'^Create_POS_Invoice$',Create_POS_Invoice,name="Create_POS_Invoice"),
		url(r'^Send_Invoice_DIAN$',Send_Invoice_DIAN,name="Send_Invoice_DIAN"),
		url(r'^Delete_Company$',Delete_Company,name="Delete_Company"),
	]
from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^List_Invoice_POS/$',List_Invoice_POS,name="List_Invoice_POS"),
		url(r'^Create_POS/$',Create_POS,name="Create_POS"),
		url(r'^Payment_Forms_POS/$',Payment_Forms_POS,name="Payment_Forms_POS"),
		url(r'^Save_Invoice_Pos/$',Save_Invoice_Pos,name="Save_Invoice_Pos"),
		url(r'^Vence_Pos/$',Vence_Pos,name="Vence_Pos"),
		url(r'^GetProducts_POS/$',GetProducts_POS,name="GetProducts_POS"),
	]
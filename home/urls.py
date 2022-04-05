from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^$',Login,name="Login"),
		url(r'^Register/$',Register,name="Register"),
		url(r'^LogOut/$',LogOut,name="LogOut"),
		url(r'^Index/$',Index,name="Index"),
		url(r'^Recoverypw/$',Recoverypw,name="Recoverypw"),
		url(r'^NewPW/(\w+)/(\w+)/$',NewPW,name="NewPW"),
		
	]
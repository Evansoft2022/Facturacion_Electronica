from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import *
from api.Create_Inventory import CreateInventory

def c(request):
	return Company.objects.get(documentIdentification = t.codificar(str(request.session['nit_company'])))


def Add_Category(request):
	global c
	if request.is_ajax():
		Category(
			name = t.codificar(str(request.GET.get('name'))),
			company = c(request)
		).save()
		return HttpResponse("")

def Add_Inventory(request):
	global c
	category = Category.objects.filter(company = c(request))
	if request.is_ajax():
		data = request.GET
		_data = {
		    "code":data['code'],
			"name":data['name'],
			"quanty":data['quanty'],
			"price":data['price'],
			"tax":data['tax'],
			"initial_inventory":data['quanty'],
		    "category":data['category'],
		    "company":request.session['nit_company']
		}
		print(_data)
		c_ = CreateInventory(_data)
		print(c_.Create())
		return HttpResponse(data)
	cat = [
		{
			'pk':c.pk,
			'name':t.decodificar(str(c.name))
		}
		for c in category
	]
	return render(request,'inventory/add.html',{'c':cat})

def List_Inventory(request):
	inv = Inventory.objects.filter(company = c(request))
	_data = [
		{
			'pk':i.pk,
			'code': t.decodificar(str(i.code)),
			'description': t.decodificar(str(i.name)),
			'quanty': t.decodificar(str(i.quanty)),
			'tax':t.decodificar(str(i.tax)),
			'price': t.decodificar(str(i.price)),
			'category':t.decodificar(str(i.category.name))

		}
		for i in inv
	]

	
	return render(request,'inventory/list_inventory.html',{'data':_data})



def Edit_Inventory(request,pk):
	i = Inventory.objects.get(company = c(request),pk = pk)
	category = Category.objects.filter(company = c(request))
	if request.is_ajax():
		data = request.GET
		i.code = t.codificar(str(data['code']))
		i.name = t.codificar(str(data['name']))
		i.price = t.codificar(str(data['price']))
		i.tax = t.codificar(str(data['tax']))
		i.quanty = t.codificar(str(data['quanty']))
		i.category = Category.objects.get(name = t.codificar(str(data['category'])))
		i.save()
		return HttpResponse()
	_data ={
		'pk':i.pk,
		'code': t.decodificar(str(i.code)),
		'description': t.decodificar(str(i.name)),
		'quanty': t.decodificar(str(i.quanty)),
		'tax':t.decodificar(str(i.tax)),
		'price': t.decodificar(str(i.price)),
		'category':t.decodificar(str(i.category.name))

	}

	cat = [
		{
			'pk':c.pk,
			'name':t.decodificar(str(c.name))
		}
		for c in category
	]

	return render(request,'inventory/edit.html',{'i':_data,'c':cat})

def Delete_Inventario(request,pk):
	Inventory.objects.get(pk = pk).delete()
	return redirect("List_Inventory")
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from .models import *
from api.translator import Translator
import time, threading, queue,json
from client.models import Client
from inventory.models import Inventory,Discount_Inventory
from django.http.request import QueryDict
from datetime import date
from api.SendInvoiceDian import send_invoice_dian
from date import Count_Days

t = Translator()
my_queue = queue.Queue()

count = 0

def storeInQueue(f):
  def wrapper(*args):
  	global my_queue
  	my_queue.put(f(*args))
  return wrapper

@storeInQueue
def Invoice_Data(request):
	company = Company.objects.get(documentIdentification = t.codificar(str(request.session['nit_company'])))
	_invoice = Invoice.objects.filter(company = company).values_list('number', flat=True).distinct()
	data = []
	for j in _invoice.order_by('-pk'):
		if j not in data:
			data.append(j)
	_data = []
	for i in data:
		_i = Invoice.objects.filter(company=company,number = i).last()
		_data.append(
				{
				'pk': t.decodificar(str(_i.number)),
				'number':t.decodificar(str(_i.prefix))+'-'+t.decodificar(str(_i.number)),
				'date': t.decodificar(str(_i.date)),
				'client':t.decodificar(str(_i.client.name)),
				'state':t.decodificar(str(_i.state)),
				'totals':round(_i.Totals())
			}
		)
	return _data

def List_Invoice(request):	
	u = threading.Thread(target=Invoice_Data,args=(request,), name='PDF')
	u.start()
	data = my_queue.get()
	if request.is_ajax():
		print(request.GET.get('pk'))
		return HttpResponse('')
	print(data)
	return render(request,'fe/list_invoice.html',{'invoice':data})

def Create_Invoice(request):
	company = Company.objects.get(documentIdentification=t.codificar(str(request.session['nit_company'])))
	client = Client.objects.filter(company = company)
	inventory = Inventory.objects.filter(company = company)
	if request.is_ajax():
		request.session['client'] = request.GET.get("pk")
		return HttpResponse(request.GET.get("pk"))
	data_client = [
									{'name':t.decodificar(str(i.name)),'code':i.pk}
									for i in client
								]

	data_inventory = [{'code':t.decodificar(str(i.code)),'name':t.decodificar(str(i.name))} for i in inventory]
	pf = Payment_Form.objects.all()
	ce = Consecutive_Elec.objects.get(company = company).number
	if 'payment_form' not in request.session:
		request.session['payment_form'] = 1
	global count
	count = 0
	return render(request,'fe/create_invoice.html',{'client':data_client,'inventory':data_inventory,'cod_bars':company.cod_bars,'pf':pf,'ce':ce})

def a(sms):
	return t.decodificar(str(sms))



def GetProducts(request):
	global count
	if request.is_ajax():
		try:
			_id = Inventory.objects.get(code = t.codificar(str(request.GET.get("pk"))))

			products = [
				{
					'pk':count,
					'code':a(_id.code),
					"name":a(_id.name),
					'cost':_id.Base_Product(),
					'tax':a(_id.tax),
					'discount':0,
					'quanty':a(_id.quanty),
					'tax_value':_id.Tax_Value()
				}
			]
			products = json.dumps(products)
			count += 1
			return HttpResponse(products)
		except Inventory.DoesNotExist:
			return HttpResponse("Error")

def Vence(request):
	if request.is_ajax():
		request.session['date_vence'] = request.GET.get('date')
		request.session['days'] = request.GET.get('days')
		return HttpResponse("")


def Save_Invoice_FE(request):
	if request.is_ajax():
		data = request.GET
		# try:
		success = False
		for i in data:
			_data = json.loads(i)
			if len(_data) == 0:
				break
			di = Discount_Inventory()
			company = Company.objects.get(documentIdentification=t.codificar(str(request.session['nit_company'])))
			consecutive = Consecutive_Elec.objects.get(company = company)
			pm = 0
			price = 0
			for j in _data:
				n = 0
				Invoice(
					number = t.codificar(str(consecutive.number)),
					prefix = t.codificar("FE"),
					code = t.codificar(str(j['Código'])),
					quanty = t.codificar(str(j['Cantidad'])),
					description = t.codificar(str(j['Descripción'])),
					price = t.codificar(str(j['Costo'])),
					tax = t.codificar(str(j['Iva'])),
					notes = t.codificar(str("No Hay")),
					date = t.codificar(str(date.today())),
					ipo = t.codificar(str(0)),
					discount = t.codificar(str(j['Desc.'])),
					client = Client.objects.get(pk = request.session['client']),
					company = company,
					state = t.codificar(str("Sin enviar a la DIAN")),
					empleoyee = Empleoyee.objects.get(pk = request.session['empleoyee_pk'])
				).save()
				

				price += float(j['Costo'])
				if n == 0:
					pm = 10 if int(request.session['payment_form']) == 1 else 30
					date_ = request.session['date_vence']
					_date = date_.split('-')
					dates = list(map(int, _date))
					days = Count_Days(dates)
					Payment_Form_Invoice(
						payment_form_id = Payment_Form.objects.get(pk = request.session['payment_form']),
						payment_method_id = Payment_Method.objects.get(_id = pm),
						payment_due_date = date.today() if pm == 10 else request.session['date_vence'],
						duration_measure = 0 if pm == 10 else days,
						invoice = Invoice.objects.filter(number = t.codificar(str(consecutive.number)),company = company).last()
					).save()

				di.Discount(int(j['Código']),int(j['Cantidad']))
			if pm == 30:
				Wallet(
					invoice = Invoice.objects.filter(number = t.codificar(str(consecutive.number)),company = company).last(),
					client = Client.objects.get(pk = request.session['client']),
					price = t.codificar(str(price)),
					date = t.codificar(str(date.today())),
					company = company
				).save()
				n += 1
				request.session['client']
			n = consecutive.number + 1
			consecutive.number = n 
			consecutive.save()
			success = True
		return HttpResponse(success)
		



def Payment_Forms(request):
	if request.is_ajax():
		request.session['payment_form'] = request.GET.get("pk")
		return HttpResponse(request.session['payment_form'])



def Print_Invoice(request):
	return render(request,'invoice.html')



@storeInQueue
def Sending(request,pk):
	sd = send_invoice_dian(pk,request.session['nit_company'])
	return sd.Send_Electronic_Invoice()



def Send_Dian(request,pk):
	u = threading.Thread(target=Sending,args=(request,pk), name='PDF')
	u.start()
	data = my_queue.get()
	print(data)
	return redirect('List_Invoice')



def Credit_Notes(request,number):
	company = Company.objects.get(documentIdentification= t.codificar(str(request.session['nit_company'])))
	invoice = Invoice.objects.filter(number = t.codificar(str(number)), company = company).last()
	Credit_Note(
		invoice = invoice,
		company = company,
		date = date.today()
	).save()
	invoice.state = t.codificar(str("Se aplico nota crédito"))
	invoice.save()
	return redirect('List_Invoice')








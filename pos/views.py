from django.http import HttpResponse
from django.shortcuts import render
from api.translator import Translator
import time, threading, queue,json
from company.models import Company
from client.models import Client
from .models import *
from inventory.models import Inventory
from data.models import *
from invoice.models import Consecutive_POS
from datetime import date

t = Translator()
my_queue = queue.Queue()

def storeInQueue(f):
  def wrapper(*args):
  	global my_queue
  	my_queue.put(f(*args))
  return wrapper


def Create_POS(request):
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
	return render(request,'pos/create_invoice.html',{'client':data_client,'inventory':data_inventory,'cod_bars':company.cod_bars,'pf':pf})



def a(sms):
	return t.decodificar(str(sms))

def GetProducts_POS(request):
	if request.is_ajax():
		try:
			_id = Inventory.objects.get(code = t.codificar(str(request.GET.get("pk"))))

			products = [
				{
					'code':a(_id.code),"name":a(_id.name),'cost':_id.Base_Product(),'tax':a(_id.tax),
					'discount':0
				}
			]
			products = json.dumps(products)
			return HttpResponse(products)
		except Inventory.DoesNotExist:
			return HttpResponse("Error")

def Vence_Pos(request):
	if request.is_ajax():
		request.session['date_vence'] = request.GET.get('date')
		request.session['days'] = request.GET.get('days')
		print('entre')
		return HttpResponse("")


def Save_Invoice_Pos(request):
	if request.is_ajax():
		data = request.GET
		try:
			success = False
			for i in data:
				_data = json.loads(i)
				if len(_data) == 0:
					break
				company = Company.objects.get(documentIdentification=t.codificar(str(request.session['nit_company'])))
				consecutive = Consecutive_POS.objects.get(company = company)
				pm = 0
				price = 0
				for j in _data:
					n = 0
					POS(
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
					).save()
					price += float(j['Costo'])
					if n == 0:
						pm = 10 if int(request.session['payment_form']) == 1 else 30
						Payment_Form_Invoice_POS(
							payment_form_id = Payment_Form.objects.get(pk = request.session['payment_form']),
							payment_method_id = Payment_Method.objects.get(_id = pm),
							payment_due_date = t.codificar(str(date.today())) if pm == 10 else request.session['date_vence'],
							duration_measure = t.codificar(str(0)) if pm == 10 else request.session['days'],
							pos = POS.objects.filter(number = t.codificar(str(consecutive.number)),company = company).last()
						).save()
				if pm == 30:
					Wallet_POS(
						pos = POS.objects.filter(number = t.codificar(str(consecutive.number)),company = company).last(),
						client = Client.objects.get(pk = request.session['client']),
						price = t.codificar(str(price)),
						date = t.codificar(str(date.today()))
					).save()
					n += 1
					request.session['client']
				n = consecutive.number + 1
				consecutive.number = n 
				consecutive.save()
				success = True
			return HttpResponse(success)
		except Exception as e:
			print(e)
			return HttpResponse(False)
		



def Payment_Forms_POS(request):
	if request.is_ajax():
		request.session['payment_form'] = request.GET.get("pk")
		print(request.session['payment_form'])
		return HttpResponse(request.session['payment_form'])


@storeInQueue
def Invoice_Data(request):
	company = Company.objects.get(documentIdentification = t.codificar(str(request.session['nit_company'])))
	_invoice = POS.objects.filter(company = company).values_list('number', flat=True).distinct()
	data = []
	for j in _invoice.order_by('-pk'):
		if j not in data:
			data.append(j)
	_data = []
	for i in data:
		_i = POS.objects.filter(company=company,number = i).last()
		_data.append(
				{
				'pk': t.decodificar(str(_i.number)),
				'number':t.decodificar(str(_i.prefix))+'-'+t.decodificar(str(_i.number)),
				'date': t.decodificar(str(_i.date)),
				'client':t.decodificar(str(_i.client.name)),
				'state':"Sin enviar a la DIAN",
				'totals':round(_i.Totals())
			}
		)
	return _data


def List_Invoice_POS(request):	
	u = threading.Thread(target=Invoice_Data,args=(request,), name='PDF')
	u.start()
	data = my_queue.get()
	return render(request,'pos/list_invoice.html',{'invoice':data})
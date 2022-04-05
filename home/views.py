from django.http import HttpResponse
from django.shortcuts import render,redirect
from company.models import Company
from api.translator import Translator
from invoice.models import Invoice
from empleoyee.models import Empleoyee
from datetime import date
from pos.models import POS
from .send_email import recoverypw
from django.utils.crypto import get_random_string
from api.models import Token

t = Translator()
intentos = 1

def LogOut(request):
	del request.session['empleoyee_pk']
	del request.session['logo_Company']
	del request.session['name_company']
	del request.session['nit_company']
	del request.session['type_empleoyee']
	return redirect('/')

def Login(request):
	global intentos
	block = False
	block_empleoyee = False
	if request.method == 'POST':

		email = t.codificar(str(request.POST.get("user")))
		pwd = t.codificar(str(request.POST.get("passwd")))
		v_e = Validate_Email(request,email)
		v_p = Validate_Pass(request,pwd)
		if v_e is not None and v_p is not None:
			user = v_e
			if not user.company.block:
				if not user.block:
					request.session['empleoyee_pk'] = user.pk
					request.session['logo_Company'] = user.company.logo.url
					request.session['name_company'] = t.decodificar(user.company.business_name)
					request.session['nit_company'] = t.decodificar(user.company.documentIdentification)
					request.session['type_empleoyee'] = t.decodificar(user.type)
					return redirect('Index')
				else:
					block_empleoyee = True
			else:
				block = True
		elif v_e is None and v_p is None:
			pass
		else:
			user_1 = v_e
			user_2 = v_p
			if not user_1.block or not user_2.block:
				if user_1 is not None and user_2 is None:
					intentos += 1
				elif user_1 is None and user_2 is not None:
					intentos += 1

				if intentos == 3:
					if user_1 is not None:
						user_1.block = True
						user_1.save()
						intentos = 0
					elif user_2 is not None:
						user_2.block = True
						user_2.save()
						intentos = 0
			else:
				block_empleoyee = True
	return render(request,'home/login.html',{'block':block,'e':block_empleoyee})


def Validate_Email(request,email):
	try:
		user = Empleoyee.objects.get(user=t.codificar(str(request.POST.get("user"))))
		return user
	except Empleoyee.DoesNotExist:
		return None

def Validate_Pass(request,pwd):
	try:
		user = Empleoyee.objects.get(passwd = t.codificar(str(request.POST.get("passwd"))))
		return user
	except Empleoyee.DoesNotExist:
		return None
	

def Register(request):
	return render(request,'home/register.html')	

def Index(request):
	total = 0
	company = Company.objects.get(documentIdentification =t.codificar(str(request.session['nit_company'])))
	invoice = Invoice.objects.filter(company = company,date = t.codificar(str(date.today())) )
	empleoyee = Empleoyee.objects.filter(company = company)
	for i in invoice:
		total += i.Totals()
	pos = POS.objects.filter(company = company, date= t.codificar(str(date.today())))
	for j in pos:
		total += j.Totals()
	return render(request,'home/index.html',{
			'invoice':len(invoice),
			'pos':len(pos),
			'totals':total,
			'empleoyee':len(empleoyee)
		}
	)

def Recoverypw(request):
	if request.method == 'POST':
		try:
			request.session['email'] = t.codificar(str(request.POST.get('email')))
			company = Empleoyee.objects.get(email = request.session['email'] )
			if company.type == t.codificar("Administrador"):
				token = get_random_string(length=96)
				Token(
					token = token
				).save()
				recoverypw(company,token)
		except Company.DoesNotExist:
			pass
	return redirect('/')

def NewPW(request,pk,token):
	if request.method == 'POST':
		try:
			company = Empleoyee.objects.get(email = request.session['email'])
			company.passwd = t.codificar(request.POST.get('passwd'))
			company.save()
			return redirect('/')
		except Company.DoesNotExist:
			pass
	try:
		token = Token.objects.get(token = token)
		token.delete()
	except Token.DoesNotExist:
		return render(request,"400.html")
	return render(request,'home/recoverpw.html')

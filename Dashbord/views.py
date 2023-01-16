from django.shortcuts import render, redirect
from .models import *
from users.models import *
import paystack
import json
import requests
from django.db.models import Q,Count
from django.conf import settings
# Create your views here.
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def form1(request):
	mode = Userinfo.objects.filter(user=request.user)
	# if request.method == "POST":
	#	pode = Form1()
	#	pode.user=request.user
	# 	pode.status = request.POST.get('stand')
	# 	pode.website_type = request.POST.get('website')
	# 	pode.project_name = request.POST.get('function')
	# 	pode.website_example = request.POST.get('website_example')
	# 	pode.db_space = request.POST.get('db_space')
	# 	pode.language_name = request.POST.get('lang')
	# 	pode.compeny_name = request.POST.get('name')
	#	pode.compeny_type = request.POST.get('compeny_type')
	# 	pode.template_name = request.POST.get('template_name')
	# 	pode.demo = request.POST.get('demo')
	# 	pode.system = request.POST.get('system')
	# 	pode.facebook = request.POST.get('facebook')
	# 	pode.instagram = request.POST.get('instagram')
	# 	pode.tweeter = request.POST.get('tweeter')
	# 	pode.gmail = request.POST.get('gmail')
	# 	pode.phone = request.POST.get('phone')
	#	mobile_whatsapp_line = request.POST.get('mobile_whatsapp_line')
	# 	pode.your_hosting = request.POST.get('your_hosting')
	# 	pode.username = request.POST.get('username')
	# 	pode.password = request.POST.get('password')
	# 	pode.first_name = request.POST.get('first_name')
	# 	pode.last_name = request.POST.get('last_name')
	# 	pode.domain_name = request.POST.get('domain_name')
	# 	pode.need_team = request.POST.get('need_team')
	# 	pode.fax_line = request.POST.get('fax_line')
	# 	pode.map_address = request.POST.get('map_address')
	# 	pode.linkedin = request.POST.get('linkedin')
	# 	pode.web_color = request.POST.get('web_color')
	# 	pode.creating_for = request.POST.get('creating_for')
	# 	pode.compeny_address = request.POST.get('compeny_address')
	# 	pode.language = request.POST.get('language')
	# 	pode.need_tutorial = request.POST.get('need_tutorial')
	# 	pode.cvv = request.POST.get('cvv')
	# 	pode.card_number = request.POST.get('card_number')
	# 	pode.card_name = request.POST.get('card_name')
	# 	pode.expire_date = request.POST.get('expire_date')
	# 	pode.card_type = request.POST.get('card_type')
	# 	pode.ssl_cert = request.POST.get('ssl_cert')
	# 	pode.server_hostname = request.POST.get('server_hostname')
	# 	pode.country = request.POST.get('country')
	# 	pode.country_code = request.POST.get('country_code')
	# 	pode.num_of_staff = request.POST.get('num_of_staff')
	# 	pode.private_email = request.POST.get('private_email')
	# 	if len(request.FILES) != 0:
	# 		pode.logo = request.FILES['image']
		# pode.save()
		# messages.success(request, 'Your Deposit have been submited Successfully')
		# return redirect('/Studio/form2')
	return render(request, 'Dashbord/form1.html',{"mode":mode})


@login_required
def pay(request):
	user_post = PayHistoryForm.objects.filter(user=request.user)
	amounts = request.GET.get('amount')
	emails = request.GET.get('email')
	pay_for = request.GET.get('pay_for')
	price = float(amounts)*100
	price = int(price)
	def init_payment(request):
		url = 'https://api.paystack.co/transaction/initialize'
		headers = {
			'Authorization': 'Bearer '+settings.PAYSTACK_SECRET_KEY,
			'Content-type' : 'application/json',
			'Accept': 'application/json',
			}
		datum = {
			"email": request.user.email,
			"amount": price
			}
		x = requests.post(url, data=json.dumps(datum), headers=headers)
		if x.status_code != 200:
			return str(x.status_code)

		result = x.json()
		return result
	initialized = init_payment(request)
	print(initialized)
	amount = price/100
	instance = PayHistoryForm.objects.create(amount=amount,user=request.user, paystack_charge_id=initialized['data']['reference'], payment_for=pay_for, paystack_access_code=initialized['data']['access_code'])
	# UserMembership.objects.filter(user=instance.user).update(reference_code=initialized['data']['reference'])
	link = initialized['data']['authorization_url']
	return HttpResponseRedirect(link)
	return render(request, 'Dashbord/pay.html',{'for':user_post})


# def call_back_url(request):
# 	reference = request.GET.get('reference')

# 	check_pay = PayHistory.objects.filter(paystack_charge_id=reference).exists()
# 	if check_pay == False:
# 		print('error')
# 	else:
# 		payment = PayHistory.objects.get(paystack_charge_id=reference)

# 		def verify_payment(request):
# 			url = 'https://api.paystack.co/transaction/verify/'+reference
# 			headers = {
# 				'Authorization': 'Bearer '+settings.PAYSTACK_SECRET_KEY,
# 				'Content-type' : 'application/json',
# 				'Accept': 'application/json',
# 				}
# 			datum = {
# 				"reference": payment.paystack_charge_id
# 				}
# 			x = requests.get(url, data=json.dumps(datum), headers=headers)
# 			if x.status_code != 200:
# 				return str(x.status_code)

# 			result = x.json()
# 			return result
# 	initialized = verify_payment(request)
# 	if initialized['data']['status'] == 'success':
# 		PayHistory.objects.filter(paystack_charge_id=initialized['data']['reference']).update(paid=True)
# 		new_payment = PayHistory.objects.get(paystack_charge_id=initialized['data']['reference'])
# 		instance = Membership.objects.get(id=new_payment.payment_for.id)
# 		sub = UserMembership.objects.filter(reference_code=initialized['data']['reference']).update(membership=instance)
# 		user_membership = UserMembership.objects.get(reference_code=initialized['data']['reference'])
# 		Subscription.objects.create(user_membership=user_membership,expires_in=dt.now().date() + timedelta(days=user_membership.membership.duration))
# 		return redirect('/payed')  
# 	return render(request, 'Dashbord/pay_ment.html') 


def payed(request):
	return render(request, 'Dashbord/payed.html')










@login_required
def form2(request):
	modes = Userinfo.objects.filter(user=request.user)
	for i in modes:
		is_ = i.creation_mode
	mode = is_
	print("this the mode",mode)
	if request.method == "POST":
		html = request.POST.get('name')
		django = request.POST.get('name_b')
		javascript = request.POST.get('name_c')
		css = request.POST.get('name_d')
		php = request.POST.get('name_e')
		laravel = request.POST.get('name_f')
		react_js = request.POST.get('name_g')
		python = request.POST.get('name_h')
		nest_js = request.POST.get('name_i')
		next_js = request.POST.get('name_j')
		bootstrap = request.POST.get('name_k')
		node_js = request.POST.get('name_l')
		ruby = request.POST.get('name_m')
		express = request.POST.get('name_n')
		ajax_js = request.POST.get('name_o')
		jqury = request.POST.get('name_p')
		material_ui = request.POST.get('name_q')
		typescript = request.POST.get('typescript')
		tailwind_css = request.POST.get('tailwind_css')
		redux = request.POST.get('redux')

		# htmls = request.POST.getlist('')
		form = Form2(user=request.user,html=html,django=django,javascript=javascript,css=css,php=php,laravel=laravel,react_js=react_js,
			python=python,nest_js=nest_js,
			next_js=next_js,bootstrap=bootstrap,node_js=node_js,ruby=ruby,express=express,ajax_js=ajax_js,jqury=jqury,material_ui=material_ui,typescript=typescript,tailwind_css=tailwind_css,redux=redux,finder_code="2222")
		form.save()
			# obj = form.save()

		return redirect('form3')
	else:
		return render(request, 'Dashbord/form2.html',{"mode":mode})
	return render(request, 'Dashbord/form2.html',{"mode":mode})
		# user = self=request.user
		# htmls = request.POST.get("html")
		# form = Form2(html=htmls)
		# form.save()
	# 	return redirect('form3')
	# else:
		# return render(request, 'Dashbord/form2.html')


# def form3(request):
# 	if request.method == "POST":
# 		futures = request.POST.getlist('file', False)
# 		g = futures.split(',')
# 		result = Futures.objects.filter(title__in=g)
# 		for u in result:
# 			print("this file here",u)
# 			print("this file here",u)
# 		# form = Form3.objects.create(user=request.user,futures=futures)
# 	tags = Futures.objects.all()
# 	return render(request, 'Dashbord/form3.html',{"tags":tags})

@login_required
def formsubmit(request):
	if request.method == "POST":
		item = Futures.objects.order_by('-item_created_date')
		query = json.loads(request.body).get('q')
		# request.GET.get('q')
		print("this th",query)
		print("this th",query)
		if query:
			data = item.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query)
			).distinct()
			print("this the value",data)
			print("this the value",data)
			print("this the value",data)
			# data = expenses.values()
			return JsonResponse(list(data), safe=False)
		else:
			return redirect('/templates')

		# search_str = json.loads(request.body).get('q')
		# expenses = Futures.objects.filter(
		# 	title__icontains=search_str) | Futures.objects.filter(
		# 	discription__icontains=search_str) | Futures.objects.filter(
		# 	tag__icontains=search_str)
		# data = expenses.values()
		# return JsonResponse(list(data), safe=False)


@login_required
def form3(request):
	if request.method == "POST":
		# search_str = json.loads(request.body).get('q')
		# expenses = Futures.objects.filter(
		# 	title__icontains=search_str) | Futures.objects.filter(
		# 	discription__icontains=search_str) | Futures.objects.filter(
		# 	tag__icontains=search_str)
		# data = expenses.values()
		# return JsonResponse(list(data), safe=False)

		future = request.POST.getlist('file', False)
		print(future)
		c = Form3(user=request.user)
		c.save()
		for i in future:
			c.futures.add(i)
		# c.save()
		
		# g = futures.split(',')
		# result = Futures.objects.filter(title__in=g)
		# for u in result:
		# 	print("this file here",u)
		# 	print("this file here",u)
		# form = Form3.objects.create(user=request.user,futures=futures)
	tags = Futures.objects.all()
	return render(request, 'Dashbord/form3.html',{"tags":tags})


def form4(request):
	if request.method == "POST":
		templat = request.POST.get('red', False)
		form = Form4(user=request.user)
		form.save()
		for i in templat:
			form.template.add(i)
			return redirect('/kwebify/form5')
	temp = template.objects.all()
	return render(request, 'Dashbord/form4.html',{"templat":temp})




def form5(request):
	return render(request, 'Dashbord/form5.html')
from django.shortcuts import render, redirect
from .models import *
from users.models import *
import paystack
import json
from django.urls import reverse
import requests
from django.db.models import Q,Count
from django.conf import settings
# Create your views here.
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.db import transaction

@login_required
def form1(request, string):
	try:
		mode = Userinfo.objects.filter(user=request.user)
		all_ = Form1.objects.filter(user=request.user)
		if all_:
			return JsonResponse({'cution': 'please click on the reset button if you wont to start new or click process to continue'})
		if request.method == "POST":
			# l = request.POST.get('num_of_staff')
			# print(l)
			request.session['website'] = request.POST.get('website','null')
			pode = Form1()			
			pode.user=request.user
			pode.status = request.POST.get('status','null')
			pode.website_type = request.POST.get('website','null')
			pode.project_name = request.POST.get('function','null')
			pode.website_example = request.POST.get('website_example','null')
			pode.db_space = request.POST.get('db_space','null')
			pode.language_name = request.POST.get('lang','null')
			pode.compeny_name = request.POST.get('name','null')
			pode.compeny_type = request.POST.get('compeny_type','null')
			pode.template_name = request.POST.get('template_name','null')
			pode.demo = request.POST.get('demo',False)
			pode.system = request.POST.get('system','null')
			pode.facebook = request.POST.get('facebook','null')
			pode.instagram = request.POST.get('instagram','null')
			pode.tweeter = request.POST.get('tweeter','null')
			pode.gmail = request.POST.get('gmail','null')
			pode.phone = request.POST.get('phone','null')
			pode.mobile_whatsapp_line = request.POST.get('mobile_whatsapp_line','null')
			pode.your_hosting = request.POST.get('your_hosting','null')
			pode.username = request.POST.get('username','null')
			pode.password = request.POST.get('password','null')
			pode.first_name = request.POST.get('first_name','null')
			pode.last_name = request.POST.get('last_name','null')
			pode.domain_name = request.POST.get('domain_name','null')
			pode.need_team = request.POST.get('need_team',False)
			pode.fax_line = request.POST.get('fax_line','null')
			pode.map_address = request.POST.get('map_address','null')
			pode.linkedin = request.POST.get('linkedin','null')
			pode.web_color = request.POST.get('web_color','null')
			pode.creating_for = request.POST.get('creating_for','null')
			pode.compeny_address = request.POST.get('compeny_address','null')
			pode.language = request.POST.get('language','null')
			pode.need_tutorial = request.POST.get('need_tutorial','null')
			pode.cvv = request.POST.get('cvv','null')
			pode.card_number = request.POST.get('card_number','null')
			pode.card_name = request.POST.get('card_name','null')
			pode.expire_date = request.POST.get('expire_date','null')
			pode.card_type = request.POST.get('card_type','null')
			pode.ssl_cert = request.POST.get('ssl_cert',False)
			pode.server_hostname = request.POST.get('server_hostname','null')
			pode.country = request.POST.get('country','null')
			pode.country_code = request.POST.get('country_code','null')
			pode.num_of_staff = request.POST.get('num_of_staff',0)
			pode.private_email = request.POST.get('private_email','null')
			if len(request.FILES) != 0:
				pode.logo = request.FILES['image']
			pode.save()
			return JsonResponse({'success': True, 'message': 'Form data submitted successfully'})
			return redirect('/Studio/form2')
	except Exception as e:
		messages.error(request, str(e))
		return JsonResponse({'success': False, 'message': 'An error occurred while processing the form'})
	return render(request, 'Dashbord/form1.html',{"mode":mode})


# def form1(request, string):
#     try:
#         mode = Userinfo.objects.filter(user=request.user)
#         if request.method == "POST":
#             form_data = request.POST.copy()
#             user = request.user  # Get the current user instance
#             form_data['user'] = user.id  # Assign the user ID to form data
			
#             # Assuming 'logo' is the name of the file input field for the image
#             form = Form1(form_data, request.FILES)
#             print(form)
#             # Check if all required fields are present
#             required_fields = ['status', 'website_type', 'project_name', 'logo']  # Add other required fields if needed
#             if all(field in form_data for field in required_fields):
#                 # Save the form instance
#                 form.save()
#                 messages.success(request, 'Your Deposit has been submitted successfully')
#                 return redirect('/Studio/form2')
#             else:
#                 messages.warning(request, 'Some required fields are missing. Please check your input.')
#     except Exception as e:
#         messages.warning(request, str(e))
	
#     return render(request, 'Dashbord/form1.html', {"mode": mode})



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
#   reference = request.GET.get('reference')

#   check_pay = PayHistory.objects.filter(paystack_charge_id=reference).exists()
#   if check_pay == False:
#     print('error')
#   else:
#     payment = PayHistory.objects.get(paystack_charge_id=reference)

#     def verify_payment(request):
#       url = 'https://api.paystack.co/transaction/verify/'+reference
#       headers = {
#         'Authorization': 'Bearer '+settings.PAYSTACK_SECRET_KEY,
#         'Content-type' : 'application/json',
#         'Accept': 'application/json',
#         }
#       datum = {
#         "reference": payment.paystack_charge_id
#         }
#       x = requests.get(url, data=json.dumps(datum), headers=headers)
#       if x.status_code != 200:
#         return str(x.status_code)

#       result = x.json()
#       return result
#   initialized = verify_payment(request)
#   if initialized['data']['status'] == 'success':
#     PayHistory.objects.filter(paystack_charge_id=initialized['data']['reference']).update(paid=True)
#     new_payment = PayHistory.objects.get(paystack_charge_id=initialized['data']['reference'])
#     instance = Membership.objects.get(id=new_payment.payment_for.id)
#     sub = UserMembership.objects.filter(reference_code=initialized['data']['reference']).update(membership=instance)
#     user_membership = UserMembership.objects.get(reference_code=initialized['data']['reference'])
#     Subscription.objects.create(user_membership=user_membership,expires_in=dt.now().date() + timedelta(days=user_membership.membership.duration))
#     return redirect('/payed')  
#   return render(request, 'Dashbord/pay_ment.html') 


def payed(request):
	return render(request, 'Dashbord/payed.html')


@login_required
def form2(request):
	mode = None
	modes = Userinfo.objects.filter(user=request.user)
	all_ = Form2.objects.filter(user=request.user)
	if all_:
		return JsonResponse({'cution': 'please click on the reset button if you wont to start new or click process to continue'})
	Languages = Language.objects.all()
	website = request.session.get('website', 'none')
	for i in modes:
		mode = i.creation_mode
		break  # Exit the loop after the first iteration
				
	if request.method == "POST":
		# Get the selected languages from the form data
		selected_languages = request.POST.getlist('selected_languages')    
		languages_list = [item.strip() for item in selected_languages[0].split(",")]
				
		# Convert the list of strings to a list of dictionaries
		languages_info = []
		for item in languages_list:
			language, version = item.split(" - ")
			languages_info.append({"language": language, "version": version})
			print(languages_info)

		# Get the Form1 instance associated with the logged-in user
		form1_instance = Form1.objects.filter(user=request.user).first()
		if not form1_instance:
			# Handle the case where no Form1 instance is found for the user
			# Redirect or display an error message
			return redirect('/studio/design/web/')
		
		# Using atomic transaction to ensure integrity
		with transaction.atomic():
			for idx, lang_info in enumerate(languages_info):
				language_name = lang_info["language"]
				version = lang_info["version"]
				
				# Create a new instance of Form2 for each language version combination
				form2_instance = Form2.objects.create(
					user=request.user,
					form1=form1_instance,
					finder_code="2222",
					language=language_name,  # Save the language directly
					version=version          # Save the version directly
				)
				
				form2_instance.save()
			
		return redirect('form3')
	else:
		return render(request, 'Dashbord/form2.html', {"mode": mode, 'website': website, 'languages': Languages})

# def form3(request):
#   if request.method == "POST":
#     futures = request.POST.getlist('file', False)
#     g = futures.split(',')
#     result = Futures.objects.filter(title__in=g)
#     for u in result:
#       print("this file here",u)
#       print("this file here",u)
#     # form = Form3.objects.create(user=request.user,futures=futures)
#   tags = Futures.objects.all()
#   return render(request, 'Dashbord/form3.html',{"tags":tags})

@login_required
def formsubmit(request):
	if request.method == "POST":
		item = Futures.objects.order_by('-item_created_date')
		query = json.loads(request.body).get('searchText')

		if query:
			data = item.filter(
				Q(title__icontains=query) |
				Q(discription__icontains=query)
			).distinct()
			
			# Serialize ImageFieldFile to its URL as a string
			data_list = [
				{
					"id": item.id,
					"Image": item.Image.url if item.Image else '',  # Convert to URL or an empty string
					"title": item.title,
					"description": item.discription
				}
				for item in data
			]
			return JsonResponse(data_list, safe=False, encoder=DjangoJSONEncoder)
		else:
			return JsonResponse([], safe=False)


		# search_str = json.loads(request.body).get('q')
		# expenses = Futures.objects.filter(
		#   title__icontains=search_str) | Futures.objects.filter(
		#   discription__icontains=search_str) | Futures.objects.filter(
		#   tag__icontains=search_str)
		# data = expenses.values()
		# return JsonResponse(list(data), safe=False)


@login_required
def form3(request):
	website = request.session.get('website', 'none')
	if request.method == "POST":
		future_ids = request.POST.getlist('file', False)
		print(future_ids)

		# Get the Form1 instance associated with the logged-in user
		form1_instance = Form1.objects.filter(user=request.user).first()
		if not form1_instance:
			# Handle the case where no Form1 instance is found for the user
			# Redirect or display an error message
			return redirect('/studio/design/web/')

		# Create a new instance of Form3
		form3_instance = Form3.objects.create(user=request.user)

		# Add each selected future to the Form3 instance
		for future_id in future_ids:
			future_instance = Futures.objects.get(id=future_id)
			form3_instance.futures.add(future_instance)

		form3_instance.save()

		return redirect('/studio/form4/')
	else:
		tags = Futures.objects.all()
		return render(request, 'Dashbord/form3.html', {'website': website, "tags": tags, "counters": tags.count()})

# @login_required
# def form4(request):
# 	website = request.session.get('website', 'none')
# 	if request.method == "POST":
# 		# selected_template_id = request.POST.get('red', None)
# 		selected_template_id = request.POST.get('selected_template', None)
# 		print("and ",selected_template_id )
# 		form3_instance = Form3.objects.filter(user=request.user).first()
# 		if not form3_instance:
# 			return HttpResponse("Form3 instance is not found for the current user.")
# 		elif not selected_template_id:
# 			return HttpResponse("Selected template ID is not provided.")
# 		form = Form4.objects.create(user=request.user, form3=form3_instance)
# 		form.template.add(selected_template_id)
# 		return redirect('/studio/form4/')
# 	else:
# 		temp = template.objects.all()
# 		return render(request, 'Dashbord/form4.html', {"templat": temp, 'website': website})


@login_required
def form4(request):
	website = request.session.get('website', 'none')
	if request.method == "POST":
		selected_template_id = request.POST.get('selected_template', None)
		# if not selected_template_id:
		# 	return JsonResponse({'error': 'Selected template ID is not provided'}, status=400)

		form3_instance = Form3.objects.filter(user=request.user).first()
		if not form3_instance:
			return JsonResponse({'error': 'Form3 instance is not found for the current user'}, status=400)

		form = Form4.objects.create(user=request.user, form3=form3_instance)
		form.template.add(selected_template_id)
		return JsonResponse({'success': True})

	else:
		templates = template.objects.all()
		return render(request, 'Dashbord/form4.html', {'templat': templates, 'website': website})



def form5(request):
	website = request.session.get('website', 'none')
	return render(request, 'Dashbord/form5.html',{'website':website})


def form6(request):
	website = request.session.get('website', 'none')
	return render(request, 'Dashbord/form6.html',{'website':website})
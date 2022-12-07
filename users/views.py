from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from users.models import *
from django.core.mail import send_mail
import math, random
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
from users.forms import ProfileUpdateForm

def generateOTP() :
	 digits = "0123456789"
	 OTP = ""
	 for i in range(4) :
		 OTP += digits[math.floor(random.random() * 10)]
	 return OTP

def send_otp(request):
	if request.method == 'POST':
		otp = request.POST['otp']
		# user = request.POST['username']
		user = request.session['username']
		if OTP.objects.filter(otp=otp).exists():
			user_ = User.objects.get(username=user)
			Userinfo.objects.filter(user=user_).update(acc_verified=True)
			OTP.objects.filter(otp=otp).delete()
			respons = 'Success! OTP matched Account succefully verified'
		else:
			respons = "Error! OTP doesn't match please check your Mail and try again !!"
		return HttpResponse(respons)

def signup(request):
	return render(request, "users/signup.html")

def create(request):
	if request.method == 'POST':
		username = request.POST['username']
		countrys = request.POST['country']
		email = request.POST['email']
		password = request.POST['password1']
		depositeds = request.POST['depositedr']
		profits = request.POST['profitr']
		bonuss = request.POST['bonusr']
		ref_bonuss = request.POST['ref_bonusr']
		balances = request.POST['balancer']
		request.session['email'] = email
		request.session['username'] = username
		if User.objects.filter(email=email).exists():
			respons = 'Error! User Account Already Exist !!'
		else:
			instance = User.objects.create(username = username, email=email, password=password,first_name='first_name', last_name='last_name')
			instance.save()
			instances = Userinfo.objects.create(user = instance, country=countrys)
			instances.save()
			inst = Userwallet.objects.create(user = instance, deposited=depositeds, profit=profits, bonus=bonuss, ref_bonus=ref_bonuss, balance=balances)
			inst.save()
			OTPs = random.randint(1000, 9000)
			OTP.objects.create(otp=OTPs,user=instance)
			mydict = {
				"email": email,
		 		"OTPs": OTPs
			}
			html_template = 'users/signup_massage.html'
			html_message = render_to_string(html_template, context=mydict)
			subject = 'Kwebify'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [email]
			message = EmailMessage(subject, html_message,
										email_from, recipient_list)
			message.content_subtype = 'html'
			message.send()
			request.session['otp'] = OTPs
			respons = 'Success! Your Account was created succefully'
		return HttpResponse(respons)
			# messages.success(request, f'Account created succefully {username}!')
			# return redirect('/login')
	else:
		form = ""
	return render(request, "users/signup.html")


def Verify_otp(request):
	if request.method == "POST":
		email = request.session['email']
		otp = request.session['otp']
		mydicts = {
			"email": email,
			"OTPs": otp
		}
		html_templates = 'users/otp.html'
		html_message = render_to_string(html_templates, context=mydicts)
		subject = 'OTP request'
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [email]
		message = EmailMessage(subject, html_message,
									email_from, recipient_list)
		message.content_subtype = 'html'
		message.send()
		success = ("Success ! OTP has been sen't to your mail")
		return HttpResponse(success)
	return render(request, "users/verify.html")


def thanku(request):
	user = request.session['username']
	user_ = User.objects.get(username=user)
	verify = Userinfo.objects.filter(user=user_)
	for verify__ in verify:
		request.session["verify_check"] = verify__.acc_verified
	return render(request,"users/thankyou2.html",{"status":request.session["verify_check"]})

def status_verify(request):
	return render(request,"users/verify_status.html")

def Onbording(request):
	if request.method == 'POST':
		user = request.session['username']
		user_ = User.objects.get(username=user)
		p_form = ProfileUpdateForm(request.POST,request.FILES,instance=user_.profile)
		if p_form.is_valid():
			p_form.save()
			messages.success(request, f'your account has been updated!')
			return redirect('/profile')
	else:
		user = request.session['username']
		user_ = User.objects.get(username=user)
		p_form = ProfileUpdateForm(instance=user_.profile)
	context={
		'p_form':p_form,
		"status":request.session["verify_check"],
		"username":request.session['username']
	}
	return render(request,"users/onboarding.html",context)
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests
import json
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *
from users.models import *
from django.db.models import Sum

@login_required
def bank(request):
	users = User.objects.all()
	history = PayHistory.objects.filter(user=request.user)
	userlist = Useraccount.objects.filter(user=request.user)
	Headeraccount = userlist.filter(default=True)
	Header = userlist.aggregate(Sum('balance'))['balance__sum']
	all_ = Useraccount.objects.filter(user=request.user)[0:4]
	wallet = Userwallet.objects.filter(user=request.user)
	coin = Usercryptowallet.objects.filter(user=request.user)
	const = {
		"Headeraccount":Headeraccount,
		"useraccounts":all_,
		"wallet":wallet,
		"Header":Header,
		"coin":coin,
		"users":users
	}
	return render(request,"kwabify/UserDashboard/finance-banks.html",const)

@login_required
def wallet(request):
	userlist = Useraccount.objects.filter(user=request.user)
	total_balance = userlist.aggregate(Sum('balance'))['balance__sum']



	wallet = Userwallet.objects.filter(user=request.user)
	kwebto = Usercryptowallet.objects.filter(user=request.user)

	userinfo = Userinfo.objects.filter(user=request.user)

	# total received count
	history = PayHistory.objects.filter(user=request.user)
	filters = history.filter(acc_type="wallet")
	total_recived = filters.filter(reason_type="received")
	user_recived = total_recived.aggregate(Sum('amount'))['amount__sum']

		# total sent count
	total_transfer = filters.filter(reason_type="transfer")
	user_transfer = total_transfer.aggregate(Sum('amount'))['amount__sum']
	# user_recived = history.filter(reason_type="received").count()
	cons = {
		"wallet":wallet,
		'total_balance':total_balance,
		"kwebto":kwebto,
		"user_recived":user_recived,
		"user_transfer":user_transfer,
	}

	return render(request,"kwabify/UserDashboard/finance-wallet.html",cons)


@login_required
def transfermoney(request):
	if request.method == "POST":
		amount = int(request.POST["amount"])
		payment_user = request.POST["user"]
		account = request.POST["accounts"]
		type_ = request.POST["type"]
		if type_ == "bank":
			user = Useraccount.objects.filter(user=request.user)
			accoutdetail = user.filter(default=True)
			for i in accoutdetail:
				accba = i.balance
			if accba < int(float(amount)):
				PayHistory.objects.create(user=request.user,payied_to=account,acc_type=type_,reason_type="transfer",reason="you dont have enough money in you Bank account Balance",status="error",amount=amount)
				response = "Sorry ! you dont have enough money in you Bank account Balance"
			else:
				if Useraccount.objects.filter(account_number=account).exists(): 
					user_acc = Useraccount.objects.filter(account_number=account)
					for i in user_acc:
						ac = float(i.balance) + amount
						use = i.user
					email = user_acc.update(balance=ac)
					user = Useraccount.objects.filter(user=request.user)
					accoutdetail = user.filter(default=True)
					for i in accoutdetail:
						accba = float(i.balance) - amount
						Useraccount.objects.filter(user=request.user).update(balance=accba)
					PayHistory.objects.create(user=request.user,payied_to=account,acc_type=type_,reason_type="transfer",reason="your transaction was succesfull",status="success",amount=amount)
					PayHistory.objects.create(user=use,payied_to=request.user.email,acc_type=type_,reason_type="received",reason="a transaction was deposited to your account",status="success",amount=amount)
					response = "Success ! your transaction was succesfull"
				else:
					PayHistory.objects.create(user=request.user,payied_to=account,acc_type=type_,reason_type="transfer",reason="You won't belive it but this is an error somthing went wrong",status="error",amount=amount)
					response = "Error ! You won't belive it but this is an error somthing went wrong"
				return HttpResponse(response)
			return HttpResponse(response)
		elif type_ == "wallet":
			user = Useraccount.objects.filter(user=request.user)
			accoutdetail = user.filter(default=True)
			for i in accoutdetail:
				accba = i.balance
			if accba < int(float(amount)):
				PayHistory.objects.create(user=request.user,payied_to=account,acc_type=type_,reason_type="transfer",reason="you dont have enough money in you Bank account Balance",status="error",amount=amount)
				response = "Sorry ! you dont have enough money in you Bank account Balance"
			else:
				if Userwallet.objects.filter(wallet_id=account).exists():
					user_wallet = Userwallet.objects.filter(wallet_id=account)
					for i in user_wallet:
						acs = float(i.balance) + amount
						use = i.user
					email = user_wallet.update(balance=acs)
					user = Useraccount.objects.filter(user=request.user,default=True)
					accoutdetail = user.filter(default=True)
					for i in accoutdetail:
						accba = float(i.balance) - amount
						Useraccount.objects.filter(user=request.user).update(balance=accba)
					PayHistory.objects.create(user=request.user,payied_to=account,acc_type=type_,reason_type="transfer",reason="your transaction was succesfull",status="success",amount=amount)
					PayHistory.objects.create(user=use,payied_to=request.user.email,acc_type=type_,reason_type="received",reason="a transaction was deposited to your account",status="success",amount=amount)
					response = "Success ! your transaction was succesfull"
				else:
					PayHistory.objects.create(user=request.user,payied_to=account,acc_type=type_,reason_type="transfer",reason="You won't belive it but this is an error somthing went wrong",status="error",amount=amount)
					response = "Error ! You won't belive it but this is an error "
			return HttpResponse(response)
		else:
			respons = "Error ! Something went Wrong please check your details"
		return HttpResponse(response)

@login_required
def wallettransfer(request):
	if request.method == "POST":
		amount = int(request.POST["amount"])
		payment_user = request.POST["user"]
		debitaccounts = request.POST["debitaccounts"]
		received_email = request.POST["email"]
		account = request.POST["accounts"]
		type_ = request.POST["type"]
		if type_ == "bank":
			user = Useraccount.objects.filter(user=request.user)
			accoutdetail = user.filter(default=True)
			for i in accoutdetail:
				accba = i.balance
			if accba < int(float(amount)):
				PayHistory.objects.create(user=request.user,payied_to=account,acc_type=type_,reason_type="transfer",reason="you dont have enough money in you Bank account Balance",status="error",amount=amount)
				response = "Sorry ! you dont have enough money in you Bank account Balance"
			else:
				if Useraccount.objects.filter(account_number=account).exists(): 
					user_acc = Useraccount.objects.filter(account_number=account)
					for i in user_acc:
						ac = float(i.balance) + amount
						use = i.user
					email = user_acc.update(balance=ac)
					user = Useraccount.objects.filter(user=request.user)
					accoutdetail = user.filter(default=True)
					for i in accoutdetail:
						accba = float(i.balance) - amount
						Useraccount.objects.filter(user=request.user).update(balance=accba)
					PayHistory.objects.create(user=request.user,payied_to=account,acc_type=type_,reason_type="transfer",reason="your transaction was succesfull",status="success",amount=amount)
					PayHistory.objects.create(user=use,payied_to=request.user.email,acc_type=type_,reason_type="received",reason="a transaction was deposited to your account",status="success",amount=amount)
					response = "Success ! your transaction was succesfull"
				else:
					PayHistory.objects.create(user=request.user,payied_to=account,acc_type=type_,reason_type="transfer",reason="You won't belive it but this is an error somthing went wrong",status="error",amount=amount)
					response = "Error ! You won't belive it but this is an error somthing went wrong"
				return HttpResponse(response)
			return HttpResponse(response)
		elif type_ == "wallet":
			user = Useraccount.objects.filter(user=request.user)
			accoutdetail = user.filter(default=True)
			for i in accoutdetail:
				accba = i.balance
			if accba < int(float(amount)):
				PayHistory.objects.create(user=request.user,payied_to=account,acc_type=type_,reason_type="transfer",reason="you dont have enough money in you Bank account Balance",status="error",amount=amount)
				response = "Sorry ! you dont have enough money in you Bank account Balance"
			else:
				if Userwallet.objects.filter(wallet_id=account).exists():
					user_wallet = Userwallet.objects.filter(wallet_id=account)
					for i in user_wallet:
						acs = float(i.balance) + amount
						use = i.user
					email = user_wallet.update(balance=acs)
					user = Useraccount.objects.filter(user=request.user,default=True)
					accoutdetail = user.filter(default=True)
					for i in accoutdetail:
						accba = float(i.balance) - amount
						Useraccount.objects.filter(user=request.user).update(balance=accba)
					PayHistory.objects.create(user=request.user,payied_to=account,acc_type=type_,reason_type="transfer",reason="your transaction was succesfull",status="success",amount=amount)
					PayHistory.objects.create(user=use,payied_to=request.user.email,acc_type=type_,reason_type="received",reason="a transaction was deposited to your account",status="success",amount=amount)
					response = "Success ! your transaction was succesfull"
				else:
					PayHistory.objects.create(user=request.user,payied_to=account,acc_type=type_,reason_type="transfer",reason="You won't belive it but this is an error somthing went wrong",status="error",amount=amount)
					response = "Error ! You won't belive it but this is an error "
			return HttpResponse(response)
		elif type_ == "kwebto":
			user = Userwallet.objects.filter(user=request.user)
			for i in user:
				kwebto_bal = i.balance
			if kwebto_bal < int(float(debitaccounts)):
				PayHistory.objects.create(user=request.user,payied_to=account,acc_type=type_,reason_type="buy",reason="you dont have enough money in you wallet account Balance",status="error",amount=debitaccounts)
				response = "Sorry ! you dont have enough money in you Bank account Balance"
			else:
				if Usercryptowallet.objects.filter(crpyto_wallet_address=account).exists():
					user_wallet = Usercryptowallet.objects.filter(crpyto_wallet_address=account)
					for i in user_wallet:
						acs = float(i.balance) + amount
						use = i.user
					email = user_wallet.update(balance=acs)
					accoutdetail = Userwallet.objects.filter(user=request.user)
					for i in accoutdetail:
						accba = float(i.balance) - float(debitaccounts)
						Userwallet.objects.filter(user=request.user).update(balance=accba)
					PayHistory.objects.create(user=request.user,payied_to=account,acc_type=type_,reason_type="buy",reason="your transaction was succesfull",status="success",amount=debitaccounts)
					PayHistory.objects.create(user=use,payied_to=request.user.email,acc_type=type_,reason_type="received",reason="a transaction was deposited to your kwebto",status="success",amount=amount)
					response = "Success ! your transaction was succesfull"
				else:
					PayHistory.objects.create(user=request.user,payied_to=account,acc_type=type_,reason_type="buy",reason="You won't belive it but this is an error somthing went wrong",status="error",amount=amount)
					response = "Error ! You won't belive it but this is an error "
			return HttpResponse(response)
		
		else:
			respons = "Error ! Something went Wrong please check your details"
		return HttpResponse(response)


@login_required
def pay(request):
	if request.method == "POST":
		prices = request.POST["price"]
		paid_to = request.POST["email"]
		account_number = request.POST["acc"]
		paid_for = request.POST["paidfor"]
		request.session['account_number'] = account_number
		request.session['paid_to'] = paid_to
		request.session['prices'] = prices
		price = float(prices)*100
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

		instance = PayHistory.objects.create(amount=int(amount), payied_to='paid_to', payment_for=paid_for, user=request.user, paystack_charge_id=initialized['data']['reference'], paystack_access_code=initialized['data']['access_code'])
		UserBank.objects.filter(user=instance.user).update(reference_code=initialized['data']['reference'])
		link = initialized['data']['authorization_url']
		respons = "Success! Your Account was created succefully"
		return HttpResponseRedirect(link)

@login_required
def call_back_url(request):
	reference = request.GET.get('reference')

	check_pay = PayHistory.objects.filter(paystack_charge_id=reference).exists()
	if check_pay == False:
		print('error')
	else:
		payment = PayHistory.objects.get(paystack_charge_id=reference)

		def verify_payment(request):
			url = 'https://api.paystack.co/transaction/verify/'+reference
			headers = {
				'Authorization': 'Bearer '+settings.PAYSTACK_SECRET_KEY,
				'Content-type' : 'application/json',
				'Accept': 'application/json',
				}
			datum = {
				"reference": payment.paystack_charge_id
				}
			x = requests.get(url, data=json.dumps(datum), headers=headers)
			if x.status_code != 200:
				return str(x.status_code)

			result = x.json()
			return result
	initialized = verify_payment(request)
	if initialized['data']['status'] == 'success':
		if Useraccount.objects.filter(account_number=account_number).exists():
			user_ = User.objects.get(username=request.user.username)
			Useraccount.objects.filter(user=user_).update(deposited=amount)
		PayHistory.objects.filter(paystack_charge_id=initialized['data']['reference']).update(paid=True)
		new_payment = PayHistory.objects.get(paystack_charge_id=initialized['data']['reference'])
		instance = Membership.objects.get(id=new_payment.payment_for.id)
		sub = UserMembership.objects.filter(reference_code=initialized['data']['reference']).update(membership=instance)
		user_membership = UserMembership.objects.get(reference_code=initialized['data']['reference'])
		Subscription.objects.create(user_membership=user_membership,expires_in=dt.now().date() + timedelta(days=user_membership.membership.duration))
		return redirect('/subscribed')  
	return render(request, 'Template/payment.html') 


def forum(request):
	forum = Forum.objects.all().order_by('-date_created')
	count = forum.count()
	futured = Forum.objects.filter(futured=True)[0:5]
	context = {
		"forum":forum,
		"count":count,
		"futured":futured,
	}
	return render(request,"kwabify/UserDashboard/forum.html",context)

def forum_details(request, id):
	furum = Forum.objects.get(id=id)
	coment = ForumComment.objects.filter(question=furum)
	profiles = coment[0:3]
	const = {
		"profiles":profiles,
		"count":profiles.count(),
		"coment":coment,
		"furum":furum,
	}
	return render(request,"kwabify/UserDashboard/forum-details.html",const)

@login_required
def liked_qustion(request, id):
	user=request.user
	Like=False
	if request.method=="POST":
		qustion_id=request.POST['qustion_id']
		get_qustion=get_object_or_404(Forum, id=qustion_id)
		if user in get_qustion.likes.all():
			get_qustion.likes.remove(user)
			Like=False
		else:
			get_qustion.likes.add(user)
			Like=True
		data={
			"liked":Like,
			"likes_count":create_comment.likes.all().count()
		}
		return JsonResponse(data, safe=False)
	return redirect(reverse("forum_details", args=[str(id)]))

@login_required
def question_comment(request, id):
	comments=False
	if request.method =="POST":
		comment=request.POST['comment']
		qus=Forum.objects.get(id=id)
		
		if comment is not None:
			create_comment=ForumComment(question=qus, user=request.user, comment=comment)
			create_comment.save()
			comments=True
			data={
			"comment":comments,
			"comment_count":get_qustion.likes.all().count()
		}
		return JsonResponse(data, safe=False)
	return redirect(reverse("forum_details", args=[str(id)]))
	# return redirect('forum_details', question_id=id)
# @login_required
# def dislike_qustion(request, id):
# 	user=request.user
# 	Like=False
# 	if request.method == "POST":
# 		qustion_id=request.POST['qustion_id']
# 		print("printing ajax id", qustion_id)
# 		watch=get_object_or_404(Forum, id=qustion_id)
# 		if user in watch.likes.all():
# 			watch.dislikes.remove(user)
# 			Dislikes=False
# 		else:
# 			if user in watch.likes.all():
# 				watch.likes.remove(user)
# 			watch.dislikes.add(user)
# 			watch.save()
# 			Dislikes=True
# 		data={
# 			"disliked":Dislikes,
# 			'dislike_count':watch.dislikes.all().count()
# 		}
# 		return JsonResponse(data, safe=False)
# 	return redirect(reverse("forum_details", args=[str(id)]))

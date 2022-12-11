from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def bank(request):
    return render(request,"kwabify/UserDashboard/finance-banks.html")

def pay(request):
    if request.methode == "POST":
        prices = request.POST[""]
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
        instance = PayHistory.objects.create(amount=amount, payment_for="deposit", user=request.user, paystack_charge_id=initialized['data']['reference'], paystack_access_code=initialized['data']['access_code'])
        UserBank.objects.filter(user=instance.user).update(reference_code=initialized['data']['reference'])
        link = initialized['data']['authorization_url']
        return HttpResponseRedirect(link)


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
		PayHistory.objects.filter(paystack_charge_id=initialized['data']['reference']).update(paid=True)
		new_payment = PayHistory.objects.get(paystack_charge_id=initialized['data']['reference'])
		instance = Membership.objects.get(id=new_payment.payment_for.id)
		sub = UserMembership.objects.filter(reference_code=initialized['data']['reference']).update(membership=instance)
		user_membership = UserMembership.objects.get(reference_code=initialized['data']['reference'])
		Subscription.objects.create(user_membership=user_membership,expires_in=dt.now().date() + timedelta(days=user_membership.membership.duration))
		return redirect('/subscribed')  
	return render(request, 'Template/payment.html') 

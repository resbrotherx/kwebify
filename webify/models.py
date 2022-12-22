from django.db import models
from django.contrib.auth.models import User

class PayHistory(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	paystack_charge_id = models.CharField(max_length=100, default='', blank=True)
	paystack_access_code = models.CharField(max_length=100, default='', blank=True)
	payment_for = models.CharField(max_length=300, default='', blank=True)
	payied_to = models.CharField(max_length=25)
	reason_type = models.CharField(max_length=60,default="", blank=True)
	reason = models.TextField(max_length=500, default="", blank=True)
	acc_type = models.CharField(max_length=60,default="", blank=True)
	# payment_for = models.ForeignKey('Membership', on_delete=models.SET_NULL, null=True)
	paid = models.BooleanField(default=False)
	status = models.CharField(max_length=15,default="", blank=True)
	amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	date = models.DateTimeField(auto_now_add=True)
	date_created = models.DateTimeField(auto_now=True)
 
	def __str__(self):
		return self.user.username

# class WalletHistory(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
# 	payment_for = models.CharField(max_length=300, default='', blank=True)
# 	payied_to = models.CharField(max_length=25)
# 	reason_type = models.CharField(max_length=60,default="", blank=True)
# 	reason = models.TextField(max_length=500, default="", blank=True)
# 	acc_type = models.CharField(max_length=60,default="", blank=True)
# 	# payment_for = models.ForeignKey('Membership', on_delete=models.SET_NULL, null=True)
# 	paid = models.BooleanField(default=False)
# 	status = models.CharField(max_length=15,default="", blank=True)
# 	amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
# 	date = models.DateTimeField(auto_now_add=True)
# 	date_created = models.DateTimeField(auto_now=True)
 
# 	def __str__(self):
# 		return self.user.username
#### User Membership
class Useraccount(models.Model):
	STATUS_CHOICES = (('income','Income'), ('expense',"Expense"), ('investment',"Investment"))
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	account_number = models.CharField(max_length=15)
	deposited = models.FloatField()
	default = models.BooleanField(default=False)
	date_updated = models.DateTimeField(auto_now_add=True)
	date_created = models.DateTimeField(auto_now=True)
	balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	acc_type = models.CharField(max_length=400, choices=STATUS_CHOICES, default='expense')

	def __str__(self):
	   return self.user.username

class Userwallet(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	deposited = models.FloatField()
	wallet_id = models.CharField(max_length=7,default="0")
	balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

	def __str__(self):
		return self.user.username


class Usercryptowallet(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	deposited = models.FloatField()
	crpyto_wallet_address = models.CharField(max_length=30)
	bonus = models.FloatField()
	ref_bonus = models.FloatField()
	balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

	def __str__(self):
		return self.user.username

# class UserBank(models.Model):
#     user = models.OneToOneField(User, related_name='user_bank', on_delete=models.CASCADE)
#     account = models.ManyToManyField(Useraccount, related_name='user_account', on_delete=models.CASCADE, null=True)
#     reference_code = models.CharField(max_length=100, default='', blank=True) 
 
#     def __str__(self):
#        return self.user.username

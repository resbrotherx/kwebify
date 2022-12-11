from django.db import models
from django.contrib.auth.models import User

class PayHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    paystack_charge_id = models.CharField(max_length=100, default='', blank=True)
    paystack_access_code = models.CharField(max_length=100, default='', blank=True)
    payment_for = models.CharField(max_length=300, default='', blank=True)
    payied_to = models.CharField(max_length=25)
    # payment_for = models.ForeignKey('Membership', on_delete=models.SET_NULL, null=True)
    paid = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.user.username

#### User Membership
class Useraccount(models.Model):
    user = models.OneToOneField(User, related_name='user_bank', on_delete=models.CASCADE)
    account_number = models.CharField(max_length=15)
    deposited = models.FloatField()
    date_updated = models.DateTimeField(auto_now_add=True)
    date_created = models.DateTimeField(auto_now=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
       return self.user.username

class Userwallet(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	deposited = models.FloatField()
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

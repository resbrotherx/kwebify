from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from datetime import datetime

now = datetime.now()

class Form1(models.Model):
	STATUS_CHOICES = (('company','Company'), ('individual',"Individual"))
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	status = models.CharField(max_length=400, choices=STATUS_CHOICES, default='company')
	website_type = models.CharField(max_length=100,blank=True,null=True)
	finder_code = models.CharField(max_length=5,blank=True,null=True)
	project_name = models.CharField(max_length=100,blank=True,null=True)
	website_example = models.CharField(max_length=100,blank=True,null=True)
	db_space = models.CharField(max_length=100,blank=True,null=True)
	# programing = models.ManyToManyField()
	logo = models.ImageField()
	mobile_whatsapp_line = models.CharField(max_length=100,blank=True,null=True)
	language_name = models.CharField(max_length=100,blank=True,null=True)
	compeny_name = models.CharField(max_length=100,blank=True,null=True)
	compeny_type = models.CharField(max_length=100,blank=True,null=True)
	# fields_needed = models.ManyToManyField()
	template_name = models.CharField(max_length=100,blank=True,null=True)
	demo = models.BooleanField(default=False)
	system = models.CharField(max_length=100,blank=True,null=True)
	facebook = models.CharField(max_length=100,blank=True,null=True)
	instagram = models.CharField(max_length=100,blank=True,null=True)
	tweeter = models.CharField(max_length=100,blank=True,null=True)
	gmail = models.CharField(max_length=100,blank=True,null=True)
	phone = models.CharField(max_length=100,blank=True,null=True)
	your_hosting = models.CharField(max_length=100,blank=True,null=True)
	username = models.CharField(max_length=100,blank=True,null=True)
	password = models.CharField(max_length=100,blank=True,null=True)
	first_name = models.CharField(max_length=100,blank=True,null=True)
	last_name = models.CharField(max_length=100,blank=True,null=True)
	domain_name = models.CharField(max_length=100,blank=True,null=True)
	need_team = models.BooleanField(default=False)
	fax_line = models.CharField(max_length=100,blank=True,null=True)
	map_address = models.CharField(max_length=100,blank=True,null=True)
	linkedin = models.CharField(max_length=100,blank=True,null=True)
	# note = models.ManyToManyField()
	web_color = models.CharField(max_length=100,blank=True,null=True)
	creating_for = models.CharField(max_length=100,blank=True,null=True)
	compeny_address = models.CharField(max_length=100,blank=True,null=True)
	language = models.CharField(max_length=100,blank=True,null=True)
	need_tutorial = models.CharField(max_length=100,blank=True,null=True)
	cvv = models.CharField(max_length=100,blank=True,null=True)
	card_number = models.CharField(max_length=100,blank=True,null=True)
	card_name = models.CharField(max_length=100,blank=True,null=True)
	expire_date = models.CharField(max_length=100,blank=True,null=True)
	card_type = models.CharField(max_length=100,blank=True,null=True)
	ssl_cert = models.BooleanField(default=False)
	server_hostname = models.CharField(max_length=100,blank=True,null=True)
	country = models.CharField(max_length=100,blank=True,null=True)
	country_code = models.CharField(max_length=100,blank=True,null=True)
	num_of_staff = models.IntegerField(blank=True, null=True)
	private_email = models.CharField(max_length=3,blank=True,null=True)


class PayHistoryForm(models.Model):
	STATUS_CHOICESD = (('awaiting','Awaiting'), ('declind',"Declind"), ('confirmed',"Confirmed"))
	STATUS_CHOICES = (('domain','Domain'),('hosting',"Hosting"),('ssl','SSL'), ('pmail',"Pmail"), ('fsd','FSD'), ('maintainers',"Maintainers"), ('orders',"Orders"))
	user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	paystack_charge_id = models.CharField(max_length=100, default='', blank=True)
	paystack_access_code = models.CharField(max_length=100, default='', blank=True)
	payment_for = models.CharField(max_length=400, choices=STATUS_CHOICES, default='orders')
	status = models.CharField(max_length=400, choices=STATUS_CHOICESD, default='awaiting')
	paid = models.BooleanField(default=False)
	amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	date = models.DateTimeField(auto_now_add=True)
 
	def __str__(self):
		return self.user.username



class Form2(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	# forma =models.ManyToManyField(Form1, blank=True)
	finder_code = models.CharField(max_length=5,blank=True,null=True)
	html = models.CharField(max_length=100,blank=True,null=True)
	django = models.CharField(max_length=100,blank=True,null=True)
	javascript = models.CharField(max_length=100,blank=True,null=True)
	css = models.CharField(max_length=100,blank=True,null=True)
	php = models.CharField(max_length=100,blank=True,null=True)
	laravel = models.CharField(max_length=100,blank=True,null=True)
	react_js = models.CharField(max_length=100,blank=True,null=True)
	python = models.CharField(max_length=100,blank=True,null=True)
	nest_js = models.CharField(max_length=100,blank=True,null=True)
	next_js = models.CharField(max_length=100,blank=True,null=True)
	bootstrap = models.CharField(max_length=100,blank=True,null=True)
	node_js = models.CharField(max_length=100,blank=True,null=True)
	ruby = models.CharField(max_length=100,blank=True,null=True)
	express = models.CharField(max_length=100,blank=True,null=True)
	ajax_js = models.CharField(max_length=100,blank=True,null=True)
	jqury = models.CharField(max_length=100,blank=True,null=True)
	material_ui = models.CharField(max_length=100,blank=True,null=True)
	typescript = models.CharField(max_length=100,blank=True,null=True)
	tailwind_css = models.CharField(max_length=100,blank=True,null=True)
	redux = models.CharField(max_length=100,blank=True,null=True)
	api = models.CharField(max_length=100,blank=True,null=True)



	def __str__(self, *args, **kwargs):
		return f'user Language request'

class Futures(models.Model):
	title = models.CharField(max_length=100)
	Image = models.ImageField(upload_to="media/dashboard")
	discription = models.TextField(max_length=90)
	tag = models.CharField(max_length=100)
	item_created_date = models.DateTimeField(auto_now=True)
	item_updated_date = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.title
	

# class Form3(models.Model):
class Form3(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	finder_code = models.CharField(max_length=5,blank=True,null=True)
	futures = models.ManyToManyField(Futures)
	published = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	# def save(self, *args, **kwargs):
	# 	if not self.id:
	# 		self.created_at = now()
	# 	self.updated_at = now()
	# 	super().save(*args, **kwargs)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return str(self.user)


class template(models.Model):
	template_name = models.CharField(max_length=100)
	template_pic = models.ImageField(upload_to="media/dashboard/templatepic")
	discription = models.TextField(max_length=90)
	your_template_demo = models.URLField(max_length = 200,blank=True,null=True)
	item_created_date = models.DateTimeField(auto_now=True)
	item_updated_date = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.template_name

class Form4(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	finder_code = models.CharField(max_length=5,blank=True,null=True)
	template = models.ManyToManyField(template)
	published = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return str(self.user)


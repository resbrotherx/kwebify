from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.
class Userinfo(models.Model):
	MODE_CHOICES = (('developer','developer'), ('enterprice',"enterprice"))
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	country = models.CharField(max_length=500)
	date = models.DateTimeField(auto_now=True)
	bvn = models.CharField(max_length=12)
	creation_mode = models.CharField(max_length=400, choices=MODE_CHOICES, default='developer')
	acc_verified = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username

class OTP(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	otp = models.CharField(max_length=4)

	def __str__(self):
		return self.otp


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.png', upload_to='profiles')
	
	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		super().save()
		img = Image.open(self.image.path)
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)

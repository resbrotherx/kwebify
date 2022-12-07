from django.contrib import admin
from .models import *

admin.site.site_header = "Resbrotherx"
admin.site.site_title = "Kwebify"
admin.site.index_title = "Kwebify"
admin.site.register(Userinfo)
admin.site.register(Userwallet)
admin.site.register(OTP)
admin.site.register(Profile)
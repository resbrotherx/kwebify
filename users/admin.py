from django.contrib import admin
from .models import *

admin.site.site_header = "Apsuni"
admin.site.site_title = "Apsuni"
admin.site.index_title = "Apsuni"
admin.site.register(Userinfo)
admin.site.register(OTP)
admin.site.register(Profile)
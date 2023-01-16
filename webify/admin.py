from django.contrib import admin
from .models import *

admin.site.site_header = "Resbrotherx"
admin.site.site_title = "Kwebify"
admin.site.index_title = "Kwebify"
admin.site.register(PayHistory)
admin.site.register(Userwallet)
admin.site.register(Useraccount)
admin.site.register(Usercryptowallet)
admin.site.register(Forum)
admin.site.register(Tags)
admin.site.register(ForumComment)

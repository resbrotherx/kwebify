from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from users import views as view
from users.forms import UserLoginForm
# from crpyto.views import index
# , authentication_form=UserLoginForm)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
     path('studio/', include('Dashbord.urls')),
    path('', include('webify.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings. STATIC_URL, document_root=settings.STATIC_ROOT)
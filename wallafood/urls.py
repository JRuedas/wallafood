from django.urls import path
from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='wallafood/login')),
    path('login', views.index, name='login'),
    path('register', views.register, name='register'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='doLogout'),
    path('addAdvert', views.addAdvert, name='addAdvert'),
    path('forbidden', views.forbidden, name='forbidden'),
    path('redirectForbidden', views.redirect_forbidden, name='redirect_forbidden'),
    path('editProfile', views.edit_profile, name='edit_profile'),
    path('deleteUser', views.delete_user, name='delete_user'),
    path('changePassword', views.change_password, name='change_password'),
    path('advertisements', views.advertisements, name='advertisements'),
    path('advertisements/search', views.findAdvertisement, name='findAdvertisement')
]
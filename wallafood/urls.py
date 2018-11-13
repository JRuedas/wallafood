from django.urls import path
from django.conf.urls import url
from django.views.generic import RedirectView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
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
    path('advertisements/search', views.findAdvertisement, name='findAdvertisement'),
    path('activate/(?P<uidb64>[0-9A-Za-z_-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
    path('reset_password/', PasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password/confirm/(?P<uidb64>[0-9A-Za-z_-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password/complete', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    ]
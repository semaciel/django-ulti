from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path("contact/", views.ContactPageView.as_view(), name="contact"),
    # path('login', views.login_user, name='login'),
    # path('register', views.register, name='register'),
    # path("logout_user", views.logout_user, name='logout_user'),
    # path('activate-user/<uidb64>/<token>',
    #      views.activate_user, name='activate'),
    #path("account/ssignup/", views.AccountSignupView.as_view(), name='account_signup_custom'),
]

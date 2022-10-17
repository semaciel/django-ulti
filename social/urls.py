from django.urls import path

from . import views


app_name = 'social'

urlpatterns = [
    # path("", index.as_view(), name="home"),
    path('', views.index, name='index'),
    path('settings/', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('like-post/', views.like_post, name='like-post'),
    path('logout/', views.logout, name='logout'),
    # path('signin/', views.signin, name='signin'),


    path('search/', views.search, name='search'),
    # path('signup/', views.signup, name='signup'),
]

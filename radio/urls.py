from django.urls import path
from . import views

app_name = 'radio'

urlpatterns = [
    path('', views.index, name='index'),
    # path('<int:pk>/', views.detail, name='detail'),
    # path('<int:pk>/favorite/', views.favorite, name='favorite'),
    # path('events/<int:pk>/', event_gallery_view, name="event_gallery"),
]

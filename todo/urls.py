from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.index, name='home'),
    path('create/', views.create_todo, name='create-todo'),
    path('todo/<id>/', views.todo_detail, name='todo'),
    path('todo-delete/<id>/', views.todo_delete, name='todo-delete'),
    path('edit-todo/<id>/', views.todo_edit, name='todo-edit'),
    path('todo-orderby/<col_pri_str>/<asc_dsc>/', views.order_by, name='todo-orderby',),
    path('todo-orderby/<col_pri_str>/', views.order_by, name='todo-orderby',),
    path('todo-filterview/<filter>/', views.complete_filter_view, name='todo-filterview',),
]

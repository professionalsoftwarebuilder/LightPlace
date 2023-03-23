# chat/urls.py
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    #path('', views.index, name='index'),
    path('list_contacts/', views.list_contacts, name='list_contacts'),
    #path('<str:room_name>/', views.room, name='room'),
    path('room/<str:room_name>', views.room, name='room'),

    path('create_dialog_chat/<int:cont_id>/', views.create_dialog_chat, name='create_dialog_chat'),

]

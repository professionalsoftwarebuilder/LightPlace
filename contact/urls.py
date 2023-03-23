from .views import contact
from django.urls import include, path

app_name = 'contact'

urlpatterns = [
    # new url definition
    path('contact/msg/', contact),
]

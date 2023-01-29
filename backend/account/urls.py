from django.urls import path 
from .endpoints import *

urlpatterns = [
    path("register_user", AddUser.as_view())
]

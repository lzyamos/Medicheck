from django.urls import path
from .views import home, logout_user, register_user, symptom_analyzer

urlpatterns = [
    path('', home, name='home'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('symptom_analyzer/', symptom_analyzer, name='symptom_analyzer'),
]

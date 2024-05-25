from django.urls import path
from authentication.views import register, login, logout_user, profile_delete, profile_detail, profile_edit

app_name = 'authentication'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout_user, name='logout_user'),
    path('profiles/<str:username>/', profile_detail, name='profile_detail'),
    path('profiles/<str:username>/edit/', profile_edit, name='profile_edit'),
    path('profiles/<str:username>/delete/', profile_delete, name='profile_delete'),
]
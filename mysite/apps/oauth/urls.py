from django.urls import path
from .views import profile_view, update_profile_view

app_name = '[mainapp]'

urlpatterns = [
    path('profile/', profile_view, name='account_profile'),
    path('profile/update/', update_profile_view, name='update_profile'),
]

from django.urls import path
from . import views



urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.view_profile, name='view_profile'),
    path('update_profile/', views.update_profile, name='update_profile')
    

]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Add this line for the home view
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),  # Add this line
]

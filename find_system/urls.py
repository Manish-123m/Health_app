from django.contrib import admin
from django.urls import path
from user_system import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),  # This is the login page
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/login/', views.login_view, name='login'),  # Explicitly add this path
]

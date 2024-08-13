"""
URL configuration for expence_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import *
from login.views import Login,register,Logout
from django.contrib.auth.views import LogoutView

app_name = 'core'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', Login, name='login'),
    path('register/', register, name='register'),
    path('expense/', expense, name='expense'),
    path('income/', income, name='income'),
    path('logout/', Logout, name='logout'),
    path('update_expense/<int:expense_id>/', update_expense, name='update_expense'),
    path('delete_expense/<int:expense_id>/', delete_expense, name='delete_expense'),
    path('delete_income/<int:incom_id>/', delete_income, name='delete_income'),
    path('update_income/<int:incom_id>/', update_income, name='update_income'),
    path('expense_summary/', expense_summary, name='expense_summary'),
    path('income_summary/', income_summary, name='income_summary'),
]

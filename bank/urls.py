"""bank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from www_bank import views, api_views
# from django.contrib.auth.views import LoginView as auth_views, LogoutView
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls.static import static
from bank import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('account/<int:account_id>/', views.get_account, name='account'),
    path('transaction/create', views.create_transaction, name='create_transaction'),
    path('transaction/<int:transaction_id>/', views.show_transaction, name='show_transaction'),
    path('reset_password/', auth_views.PasswordResetView.as_view(),
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
    path('reset_password_complete/login/', views.index),
    path('transaction/all/', views.all_transactions, name='all_transactions'),
    path('api/login/', jwt_views.TokenObtainPairView.as_view(), name='api_login'),
    path('api/refresh/', jwt_views.TokenRefreshView.as_view(), name='api_refresh'),
    path('api/verify/', jwt_views.TokenVerifyView.as_view(), name='api_verify'),
    path('api/transaction/<int:transaction_id>/', api_views.show_transaction),
    path('api/transaction/<int:transaction_id>/accept/', api_views.accept_transaction),
    path('api/transaction/<int:transaction_id>/delete/', api_views.delete_transaction),
    path('api/account/<int:account_id>/', api_views.show_account),
    path('api/transaction/all/', api_views.show_full_transaction),
    path('api/account/<int:account_id>/transactions/', api_views.show_all_transactions),
    path('api/register/', api_views.register) 

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

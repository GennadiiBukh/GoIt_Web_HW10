from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.quotes_list, name='quotes_list'),
    path('<int:pk>/', views.quote_detail, name='quote_detail'),
    path('author/<int:pk>/', views.author_detail, name='author_detail'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
]
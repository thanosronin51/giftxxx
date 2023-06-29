from django.urls import path
from .import views

urlpatterns=[
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('change_password_view', views.change_password_view, name='change_password_view'),
    path('make_payment', views.make_payment, name='make_payment'),
    path('payment_success', views.payment_success, name='payment_success'),
    path('select_user', views.select_user, name='select_user'),
]


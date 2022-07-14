from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('create/<str:session_id>', views.create, name="create"),
    path('login', views.login_view, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout_view, name="logout"),
    path('response/<str:session>', views.response, name="response"),
    path('analytics/<str:session>', views.analytics, name="analytics"),
    path('warning', views.warning, name="warning")
]

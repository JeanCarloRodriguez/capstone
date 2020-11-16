
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_merchandise", views.addMerchandise, name="addMerchandise"),
    path("showMerchandise/<str:code>", views.showMerchandise, name="showMerchandise"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


    # API URL
    path("getMerchandise/<str:merchandise_id>", views.getMerchandise, name="getMerchandise")
]
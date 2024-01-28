from django.urls import path

from . import views

urlpatterns = [
    path("", views.active_listing, name="active_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("selected_listing", views.selected_listing, name="selected_listing"),
    path("end_listing", views.end_listing, name="end_listing"),
    path("watch", views.watch, name="watch"),
    path("categories", views.categories, name="categories")
    
]

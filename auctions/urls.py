from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("new/", views.create_listing, name="new"),
    path("<int:id>/home/", views.home, name="home"),
    path("<str:title>/", views.listing, name="listing"),
    path("<str:title>/bid/", views.bid, name="bid"),
    path('<str:title>/watchlist/', views.add_watchlist, name="watchlist"),
    path('<str:title>/close/', views.close_listing, name="close")

]

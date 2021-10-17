from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("new/", views.create_listing, name="new"),
    path("<int:user_id>/home/", views.home, name="home"),
    path("<int:listing_id>/", views.listing, name="listing"),
    path('<int:listing_id>/watchlist/', views.watchlist, name="watchlist"),
    path('<int:listing_id>/close/', views.close_listing, name="close"),
    path('<int:listing_id>/comment/', views.add_comments, name='comment'),
    path('<str:category>/category/', views.category, name='category'),

]

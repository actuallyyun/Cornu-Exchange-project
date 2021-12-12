from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("new/", views.create_listing, name="new"),
    path("<int:user_id>/home/", views.home, name="home"),
    path("listings/<int:listing_id>/", views.listing, name="listing"),
    path('watchlist/<int:listing_id>/', views.watchlist, name="watchlist"),
    path('close/<int:listing_id>/', views.close_listing, name="close"),
    path('comment/<int:listing_id>/', views.add_comments, name='comment'),
    path('category/<str:category>/', views.category, name='category'),

]

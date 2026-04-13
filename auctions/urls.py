from django.urls import path,include
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create_listing,name="create"),
    path("homepage", views.listing, name="homepage"),  
    path("homepage/<int:id>/", views.listing, name="listing"),  
    path("watchlist/<int:id>/", views.watchlist_view, name="watchlist"),
    path("watchlist/", views.watchlist_page, name="watchlist_page"),
    path("bidding/<int:id>/", views.bidding, name="bidding"),
    path("close/<int:id>/", views.close_auction, name="close_auction"),
    path("category", views.categories, name="category"),
    path("category/<str:category>/", views.cate, name="cate"),
    





]

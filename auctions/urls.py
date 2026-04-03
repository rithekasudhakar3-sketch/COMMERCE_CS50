from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create_listing,name="create"),
    path("homepage", views.listing, name="homepage"),  
    path("homepage/<int:id>/", views.listing, name="listing"),  
    path("bidding/<int:id>/", views.bidding, name="bidding"),  
    path("watchlist/", views.watchlist_page, name="watchlist"),
    path("watchlist/<int:id>/", views.watchlist_page, name="watchlist_view"),

]

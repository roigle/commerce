from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("register", views.register, name="register"),
    path("listing/<str:product_title>", views.productpage, name="productpage"),
    path("listing/<str:product_title>/<str:message>", views.productpage, name="productpage"),
    path("watchlistaddremove/<str:product_title>", views.watchlistaddremove, name="watchlistaddremove"),
    path("closelisting/<str:product_title>", views.closelisting, name="closelisting"),
    path("bidding/<str:product_title>", views.bidding, name="bidding"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.categories, name="categories"),
    path("comments/<str:product_title>", views.comments, name="comments"),
    path("newlisting", views.newlisting, name="newlisting")
]
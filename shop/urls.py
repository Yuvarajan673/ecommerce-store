from django.urls import path
from .import views

urlpatterns= [
    path('', views.home, name="home"),
    path('login/', views.loginpage, name="login"),
    path('logout', views.logoutpage, name="logout"),
    path('registration', views.registration, name="registration"),
    path('profileimage', views.profileimage, name='profileimage'),
    path('proimgremove', views.proimgremove, name='proimgremove'),
    path('repass', views.repass, name="repass"),
    path('categories', views.categories, name="categories"),
    path('products/<str:name>', views.products, name="products"),
    path('pdetails/<str:cname>/<str:pname>', views.pdetails, name="pdetails"),
    path('addtocart', views.add_to_cart, name="addtocart"),
    path('cart', views.cart_page, name="cart"),
    path('remove_cart/<str:cid>', views.remove_cart, name="remove_cart"),
]

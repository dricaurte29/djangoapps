from django.contrib import admin
from django.urls import path
from productosApp import views



urlpatterns = [
    path('',views.productos, name="productos"),
    path('/categorias/<str:cate>/',views.categorias, name="categorias"),
    path('/vista/<int:producto_id>/',views.solo, name="solo"),
    path('/tienda/<int:tienda_id>/',views.tiend, name="tienda"),
    path('/form/<int:tienda_id>/',views.form, name="form"),
    path('/eliminar/<int:tienda_id>/<int:producto_id>/',views.elimi, name="elimi"),
    path('/edit/<int:tienda_id>/<int:producto_id>/',views.edit, name="edit"),
    path('/pedi/<int:tienda_id>/<int:producto_id>/',views.pedidos, name="pedido")

]


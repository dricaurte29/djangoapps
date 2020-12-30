
from django.urls import path
from proyectoApp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home, name="inicio"),
    
    path('tiendas',views.tiendas, name="tiendas"),
    path('mitienda/<int:us_id>/',views.tiendash, name="mistiendas"),
    path('dashboard/<int:tienda_id>/',views.dashboard, name="dashboard"),
    path('pedidos/<int:tienda_id>/',views.pedi, name="pedidos"),
    path('cn/<int:producto_id>/',views.modalel, name="modalel"),
    path('ped/<int:pedido_id>/',views.modalpe, name="modalpe"),
    path('entra', views.entra , name="entra"),
    path('salir', views.salir , name="salir"),
    path('registro', views.registro, name="registro"),
    path('contacto',views.contacto, name="contacto"),
    
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


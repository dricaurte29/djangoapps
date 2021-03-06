from django.db import models
from django.contrib.auth.models import User


class tienda(models.Model):
    nombre=models.CharField(max_length=50)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)
    descripcion=models.CharField(max_length=100)
    autor=models.ForeignKey(User, related_name='tiendas', on_delete=models.CASCADE)
    instagram_link=models.CharField(max_length=255)
    whatsapp_link=models.CharField(max_length=255)
    facebook_link=models.CharField(max_length=255)
    foto_perfil=models.ImageField(upload_to='fototd')
    foto_fondo=models.ImageField(upload_to='fototd')
    ubicacion =models.CharField(max_length=30)
    class meta:
        verbose_name='tienda'
        verbose_name_plural='tiendas'
    def __str__(self):
        return self.nombre
class categoria(models.Model):
    nombre=models.CharField(max_length=50)


    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)
    
    class meta:
        verbose_name='categoria'
        verbose_name_plural='categorias'

    def __str__(self):
        return self.nombre

class producto(models.Model):
    titulo=models.CharField(max_length=50)
    contenido=models.CharField(max_length=100)
    imagen=models.ImageField(upload_to='fotopr')
    imagen2=models.ImageField(upload_to='fotopr',blank=True)
    imagen3=models.ImageField(upload_to='fotopr',blank=True)
    tienda=models.ForeignKey(tienda, related_name='productos', on_delete=models.CASCADE)
    categoria=models.ForeignKey(categoria, related_name='productos', on_delete=models.CASCADE)
    categorian=models.CharField(max_length=25)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)
    precio=models.IntegerField()

    class meta:
        verbose_name='post'
        verbose_name_plural='postes'

    def __str__(self):
        return self.titulo

class pedido(models.Model):
    item = models.ForeignKey(producto, related_name='producto', on_delete=models.CASCADE)
    cliente = models.ForeignKey(User, related_name='pedidos', on_delete=models.CASCADE)
    local = models.ForeignKey(tienda, related_name='pedidos', on_delete=models.CASCADE)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    detalle = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    contacto = models.IntegerField()
    enviado = models.BooleanField()

    class meta:
        verbose_name='pedido'
        verbose_name_plural='pedidos'

    def __str__(self):
        return self.item.titulo
class comentario(models.Model):
    item = models.ForeignKey(producto, related_name='product', on_delete=models.CASCADE)
    autor = models.ForeignKey(User, related_name='comentarios', on_delete=models.CASCADE)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)
    contenido=models.CharField(max_length=140)
    class meta:
        verbose_name='comentario'
        verbose_name_plural='comentarios'

    def __str__(self):
        return self.item.titulo







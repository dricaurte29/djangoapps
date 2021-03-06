from django.shortcuts import render, HttpResponse, redirect
from productosApp.models import producto, categoria, tienda, pedido, comentario
from django.contrib.auth.models import User
from django.db.models import Q
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.http import Http404


def send_email(pe):
    template = get_template('correo.html')
    mail = pe.local.autor.email
    product = pe.item
    cl = User()
    cl = pe.cliente
    content = template.render({"producto":product,"pedido":pe,"cliente":cl})
    email = EmailMultiAlternatives(
        'Nuevo Pedido',
        'Proyecto Eva-01',
        'muestrastore@gmail.com',
        [mail]
    )
    print(mail)
    email.attach_alternative(content, 'text/html')
    email.send()
    print(email)





def productos(request):
    
    
    categorias=categoria.objects.all()
    page = request.GET.get('page',1)
    busqueda = request.GET.get('bus')
    nbn = 0
    if busqueda:
        
        productos = producto.objects.filter(
            Q(titulo__icontains=busqueda) |
            Q(contenido__icontains=busqueda) |
            Q(categorian__icontains=busqueda)
            ).distinct()
        nbn = productos.count()
    else:
        productos=producto.objects.all()


    try:
            paginator = Paginator(productos, 6)
            productos = paginator.page(page)
    except:
        raise Http404      
    return render(request, "productos.html", {"nbn":nbn,"nb":busqueda,"entity": productos, "categorias": categorias,"paginator":paginator})

def categorias(request, cate):
    
    busqueda=categoria.objects.get(nombre= cate)
    productos=producto.objects.filter(categoria=busqueda)
    categorias=categoria.objects.all()
    return render(request, "buspro.html", {"productos": productos, "categorias": categorias, "categoria": busqueda})

def solo(request, producto_id):

    product=producto.objects.get(id= producto_id)
    comentarios = comentario.objects.filter(item_id= producto_id)
    print(product.tienda_id)
    ids= product.tienda_id
    tien=tienda.objects.get(id=ids)
    page = request.GET.get('page',1)
    try:
            paginator = Paginator(comentarios, 3)
            comentarios = paginator.page(page)
    except:
        raise Http404 
    if request.method == 'POST':
        
        pe = pedido()
        pe.item = product
        pe.cantidad = int(request.POST.get('cantidad'))
        pe.contacto = int(request.POST.get('contacto'))
        pe.direccion = request.POST.get('direccion')
        pe.detalle = request.POST.get('detalle')
        pe.precio = int(request.POST.get('total'))
        pe.enviado = False
        us = User()
        us.id = int(request.POST.get('usid'))
        pe.cliente = us
        pe.local = tien
        pe.save()
        send_email(pe)
        return render(request, "confirma.html",{ "tienda":tien })
    return render(request, "solo.html",{"producto":product, "tienda":tien ,"entity":comentarios})

def pedidos(request, tienda_id, producto_id):
    tien = tienda.objects.get(id = tienda_id)
    product=producto.objects.get(id= producto_id)
    if request.method == 'POST':
        print('printing POST::: ', request.POST)
        pe = pedido()
        pe.item = product
        pe.cantidad = int(request.POST.get('cantidad'))
        pe.contacto = int(request.POST.get('contacto'))
        pe.direccion = request.POST.get('direccion')
        pe.detalle = request.POST.get('detalle')
        pe.precio = int(request.POST.get('total'))
        us = User()
        us.id = int(request.POST.get('usid'))
        pe.cliente = us
        pe.local = tien
        pe.save()

        return redirect('/entra')



    return render(request, "pedido.html",{"producto":product})

def tiend(request, tienda_id):

    tien=tienda.objects.get(id= tienda_id)
    categorias=categoria.objects.all()
    productos=producto.objects.filter(tienda_id= tienda_id)
    return render(request, "tienda.html",{"tienda":tien, "categorias": categorias, "productos":productos})

def elimi(request, tienda_id, producto_id):

    prd = producto.objects.get(id= producto_id)
    prd.delete()
    return redirect('dashboard', tienda_id= tienda_id)

def edit(request, tienda_id, producto_id):
    prd = producto.objects.get(id= producto_id)
    categorias=categoria.objects.all()
    tien=tienda.objects.get(id= tienda_id)
    if request.method == 'POST':
        
        prd.titulo = request.POST.get('nombre')
        prd.contenido = request.POST.get('contenido')
        prd.precio = int(request.POST.get('precio'))
        if request.POST.get('imagen') == "":
            print("NO IMAGEN :(")
        else:
            print(request.FILES.get('imagen'))
            prd.imagen = request.FILES.get('imagen')

        

        cat = categoria()
        cat.id = int(request.POST.get('categoria'))
        prd.categoria = cat 
        prd.save()


        #print('printing POST::: ', request.POST)
        return redirect('dashboard', tienda_id= tienda_id)
    return render(request, "edit.html", {"tienda": tien, "categorias":categorias, "producto":prd})

def form(request, tienda_id):
    categorias=categoria.objects.all()
    tien=tienda.objects.get(id= tienda_id)
    if request.method == 'POST':
        pr = producto()
        pr.titulo = request.POST.get('nombre')
        pr.contenido = request.POST.get('contenido')
        pr.precio = int(request.POST.get('precio'))
        pr.imagen = request.FILES.get('imagen')
        tn = tienda()
        tn.id = tienda_id
        pr.tienda = tn
        cat = categoria()
        cat.id = int(request.POST.get('categoria'))
        pr.categoria = cat 
        pr.save()

        print('printing POST::: ', request.POST)
        return redirect('dashboard', tienda_id= tienda_id)
    return render(request, "formpro.html", {"tienda": tien, "categorias":categorias})
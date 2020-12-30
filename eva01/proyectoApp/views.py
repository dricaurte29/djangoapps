from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import usuariof
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from productosApp.models import producto, categoria, tienda, pedido
from django.core.paginator import Paginator
from django.http import Http404


def home(request):
    categorias=categoria.objects.all()
    productos=producto.objects.all()
    tiendas=tienda.objects.all()
    return render(request, "proyectoApp/inicio.html", {"productos": productos, "categorias": categorias, "tiendas": tiendas})



def tiendas(request):
    tien=tienda.objects.all()
    page = request.GET.get('page',1)
    busqueda = request.GET.get('bus')
    if busqueda:
        
        tien = tienda.objects.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) 
            ).distinct()
    try:
            paginator = Paginator(tien, 3)
            tien = paginator.page(page)
    except:
        raise Http404
    return render(request, "proyectoApp/tienda.html", {"entity":tien,"paginator":paginator})

def tiendash(request, us_id):
    tien=tienda.objects.filter(autor_id= us_id)
    return render(request, "proyectoApp/tiendash.html", {"tiendas":tien})


     
def dashboard(request, tienda_id):
    tien=tienda.objects.get(id= tienda_id)
    productos=producto.objects.filter(tienda_id= tienda_id)
    ped = pedido.objects.filter(local_id=tienda_id)
    pc = ped.count()
    return render(request, "proyectoApp/dashboard.html", {"tienda":tien, "productos":productos, "pc":pc})

def pedi(request, tienda_id):
    tien=tienda.objects.get(id= tienda_id)
    pedidos=pedido.objects.filter(local_id =tienda_id)
    page = request.GET.get('page',1)
    pc = pedidos.count()

    try:
        paginator = Paginator(pedidos, 3)
        pedidos = paginator.page(page)
    except:
        raise Http404
    
    return render(request, "proyectoApp/pedidos.html", {"tienda":tien, "entity":pedidos, "paginator":paginator,"pc":pc})


    
    
def contacto(request):


    return render(request, "proyectoApp/contacto.html")

def modalel(request, producto_id):
    pro = producto.objects.get(id=producto_id)

    return render(request, "proyectoApp/modalel.html", {"producto":pro})

def modalpe(request, pedido_id):
    ped = pedido.objects.get(id=pedido_id)

    return render(request, "proyectoApp/modalpe.html", {"pedido":ped})

def registro(request):
    form = usuariof(data=request.POST)
    
    if request.method == 'POST':
        try:
            form.save()
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Bien hecho")  
            return redirect('/')
        except:
            messages.info(request, "Datos erroneos")
            return redirect('/registro')
    return render(request, "proyectoApp/registro.html",{"form":usuariof()})

def salir(request):

    logout(request)
    messages.success(request, "Saliste")

    return redirect('/entra')

def entra(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            clave = form.cleaned_data.get('password')
            user = authenticate(username=usuario, password=clave)
            if user is not None:
                login(request, user)
                messages.success(request, f"estas adentro {user.username}")
                return redirect('/')
            else:
                messages.info(request, "Datos incorrectos")
        else:
            messages.info(request, "Datos incorrectos")
    form = AuthenticationForm()
    return render(request, "proyectoApp/entra.html", {"form": form})
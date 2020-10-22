from django.shortcuts import render, redirect,HttpResponse,HttpResponseRedirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View
from django.contrib.auth.forms import User
from proyecto.app.inicio.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user is not None and user.is_staff:
                do_login(request, user)
                return redirect("/dashboard")
            messages.error(request,'Error, Contactese con el administrador para resolver el problema gracias.')
            return redirect('/')
        else:
            messages.error(request,'Error, datos incorrectos intente nuevamente gracias.')
        return redirect('/')
    return render(request,"inicio/login.html") 


def dashboard(request):
    if request.user.is_authenticated:
        #user = request.user
        return render(request,"inicio/dashboard.html")
    return redirect("/")

def cerrarSesion(request):
    do_logout(request)
    return redirect("/")

""" def getUsers(request):
    users = User.objects.all().order_by('-id')
    return render(request,'inicio/getUsers.html' , {'users':users}) """

class AllGetUsers(View):
    model = User
    template_name = 'inicio/getUsers.html'
    
    def get_queryset(self):
        #si quiero enviar otra consulta
        return self.model.objects.all()
    
    def get_context_data(self, **kwargs):
        context = {}
        context['users'] = self.get_queryset()
        #PUEDO AGREGAR MAS DATOS EL CONTEXTO contexto['otros']
        return context
    
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name, self.get_context_data())
    


from django.http import JsonResponse
def registerNewUser(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                return HttpResponse('200')
    #form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    #form.fields['password2'].help_text = None
    return render(request,"inicio/registerNewUser.html",{'form':form})
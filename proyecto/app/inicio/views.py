from django.shortcuts import render, redirect,HttpResponse,HttpResponseRedirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View, DetailView
from django.contrib.auth.forms import User
from proyecto.app.inicio.forms import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
        dic = {
            'users':self.model.objects.all(),
            #'usuarios':self.model.objects.all().count()
        }
        return dic
    
    def get_context_data(self, **kwargs):
        context = self.get_queryset()
        #print(context)
        #PUEDO AGREGAR MAS DATOS EL CONTEXTO contexto['otros']
        return context
    
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name, self.get_context_data())
    


class UserDetailView(DetailView):
    model = User
    template_name = "inicio/user.html"
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        #print(request.POST['checkbox'])#obtengo un dato de un input del formulario
        #print(kwargs['pk'])#diccionario de datos para obtener los datos del la url
        get_user = User.objects.get(pk = kwargs['pk'])
        if request.POST['option'] == "0":
            get_user.is_active=True
            get_user.is_staff=False
            get_user.is_superuser=False
            get_user.save()
            return HttpResponse('El suario se dió de baja exitosamente')
            #print(get_user.is_staff)
        #print(type(args))#tupla de datos se encuentra vacio
        
        elif request.POST['option'] == 'super':
            get_user.is_active=True
            get_user.is_staff=True
            get_user.is_superuser=True
            get_user.save()
            return HttpResponse('Se habilitó como superuser')
        elif request.POST['option'] == 'user':
            get_user.is_active=True
            get_user.is_staff=True
            get_user.is_superuser=False
            get_user.save()
            return HttpResponse('Se habilitó como usuario')

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

    
def MyPerfilUser(request):
    if request.method=='POST':
        user_form=UserForms(request.POST,instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your password was updated successfully!')
            #return render(request,'inicio/updateUser.html')  
            return HttpResponse("tus datos se actualizaron correctamente!")
    else:
        user_form=UserForms(instance=request.user)
        return render(request,'inicio/updateUser.html',{'user_form':user_form})

@login_required(login_url='/')
def ChangePassword(request, id_user):
	if request.method=='POST':
		form=ChangePasswordForm(request.POST)
		new_password = request.POST['new_password']
		confirmed = request.POST['confirm_password']
		user = request.user
		print(user.check_password(request.POST['old_password']))
		if new_password == confirmed and user.check_password(request.POST['old_password']):
			user.set_password(new_password)
			user.save()
			print('bien')
			return HttpResponse("success")
		else:
			return HttpResponse("error")
	else:
		form=ChangePasswordForm()
	return render(request,'inicio/changePassword.html',{'form':form})
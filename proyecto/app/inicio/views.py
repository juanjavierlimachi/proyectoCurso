from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return render(request,'inicio/index.html')


def dashboard(request):

    return render(request, 'inicio/dashboard.html')
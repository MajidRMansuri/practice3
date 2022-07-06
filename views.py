# from django.http import HttpResponse
from atexit import register
from doctest import master
from email.policy import default
from django.shortcuts import redirect, render
from .models import Master
default_data = {}
# Create your views here.


def index(request):
    # return HttpResponse('<h1>Hello</h1>')
    user_data()
    # remove_item(request)
    return render(request,'index.html',default_data)

def form_data(request):
    Master.objects.create(
        Name = request.POST['name'],
        Email = request.POST['email'],
        Password = request.POST['password'],
    )
    return redirect(index)

def login_page(request):
    return render(request, 'login_page.html')
    user_data()

def login(request):
    try:
        master = Master.objects.get(Email = request.POST['email'])

        if master.Password == request.POST['password']:
            print('login Successfully')
            request.session['email'] = master.Email
            return redirect(profile)
        else:
            print('incorrect Password')
    except Master.DoesNotExist as err:
        print(err)

def profile(request):
#     master = register.object.get(Email = request.session['email'])
#     data['data'] = master
    default_data['current_page'] = 'profile'
    profile_data(request)
    return render(request, 'profile.html', default_data)

def profile_data(request):
    master = Master.objects.get(Email = request.session['email'])
    default_data['profile_data'] = master

def update_form_data(request):
    master = Master.objects.get(Email = request.session['email'])

    master.Name = request.POST['name']
    master.Email = request.POST['email']
    master.Password = request.POST['password']

    master.save()
    return redirect(profile)

def user_data():
    default_data['user_items'] = Master.objects.all()

def edit_item(request, pk):
    master = Master.objects.get(id=pk)

    if request.POST:
        master.Name = request.POST['name']
        master.Email = request.POST['email']
        master.Password = request.POST['password']
        master.save()
    else:
        default_data['edit_user_item'] = master
    return redirect(index)

def remove_item(request, pk):
    Master.objects.get(id=pk).delete()
    return redirect(index)
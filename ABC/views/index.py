from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def index(request):
    return render(request, 'ABC/index.html')


def signin(request):
    return render(request, 'ABC/signin.html')


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('index')

    context = {'message': 'Invalid Username/Password'}
    # I should invoke directly to the view with the context
    return render(request, 'ABC/signin.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

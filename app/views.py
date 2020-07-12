from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from app.forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required



User = get_user_model()

# Create your views here.
@login_required(login_url='/login/')
def index(request):
    return render(request, 'app/index.html', {})


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'form': form
    }
    print(request.user.is_authenticated)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            print("error.......")

    return render(request, "auth/login.html", context=context)




def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        'form': form,
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password_first")
        new_user = User.objects.create_user(username, email, password)
    return render(request, "auth/register.html", context=context)




def logout_page(request):
    print(request)
    logout(request)
    return redirect('/')





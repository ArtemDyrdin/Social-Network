from django.shortcuts import render, redirect
from .forms import AuthUserForm
from django.contrib.auth.models import User

from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login

from django.http import HttpResponseForbidden


def main(request):
    data = {
        'title': 'Welcome'
    }
    return render(request, 'network/index.html', data)


def account(request):
    data = {
        'title': 'Account'
    }
    return render(request, 'network/account.html', data)


def register(request):
    if request.user.is_authenticated:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            # form = RegisterUserForm(request.POST)
            # if form.is_valid():
            #     user = form.save()

            #     username = form.cleaned_data['username']
            # password = form.cleaned_data['password']
            #     email = form.cleaned_data['email']
            #     first_name = form.cleaned_data['first_name']
            #     last_name = form.cleaned_data['last_name']
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            # auth_user = authenticate(
            #     username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            # login(request, auth_user)
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name)
            return redirect('account')

        # else:
        #     form = RegisterUserForm()

        dt = {
            # 'form': form,
            'title': 'Sign up'
        }

        return render(request, 'network/signup.html', dt)


class LogInView(LoginView):
    template_name = 'network/signin.html'
    form_class = AuthUserForm
    success_url = '/account'

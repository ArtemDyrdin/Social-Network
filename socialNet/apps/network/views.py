from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.urls import reverse

from .forms import AuthUserForm, RegisterUserForm, MessageForm
from .models import Chat, Message
from django.views import View

from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login

from django.db.models import Count


def main(request):
    if request.user.is_authenticated:
        return HttpResponseForbidden()
    else:
        data = {
            'title': 'Welcome'
        }
        return render(request, 'network/index.html', data)


def account(request):
    data = {
        'title': 'Account'
    }
    return render(request, 'network/account.html', data)


def friends(request):
    User = get_user_model()
    users = User.objects.all()
    data = {
        'title': 'Friends',
        'users': users
    }
    return render(request, 'network/friends.html', data)


def person(request, pk):
    User = get_user_model()
    person = User.objects.get(id=pk)
    title = person.first_name + ' ' + person.last_name
    data = {
        'title': title,
        'person': person
    }
    return render(request, 'network/person.html', data)


class CreateDialogView(View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[
                                    request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        print(f'\n', chat.id, '\n')
        return redirect(reverse('messages', kwargs={'chat_id': chat.id}))
        # return redirect(reverse('messages'))


class MessagesView(View):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_readed=False).exclude(
                    author=request.user).update(is_readed=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        return render(
            request,
            'network/dialog.html',
            {
                'user_profile': request.user,
                'chat': chat,
                'form': MessageForm()
            }
        )

    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('messages', kwargs={'chat_id': chat_id}))


class DialogsView(View):
    def get(self, request):
        chats = Chat.objects.filter(members__in=[request.user.id])
        return render(request, 'network/chats.html', {'user_profile': request.user, 'chats': chats})


def register(request):
    if request.user.is_authenticated:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                user = form.save()

                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                auth_user = authenticate(
                    username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                login(request, auth_user)

                return redirect('account')

        else:
            form = RegisterUserForm()

        dt = {
            'form': form,
            'title': 'Sign up'
        }

        return render(request, 'network/signup.html', dt)


class LogInView(LoginView):
    template_name = 'network/signin.html'
    form_class = AuthUserForm
    success_url = '/account'

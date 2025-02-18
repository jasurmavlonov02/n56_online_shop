from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.views.generic import FormView

from user.forms import LoginForm, RegisterForm
from config.settings import DEFAULT_FROM_EMAIL


# Create your views here.


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('shop:products')
            else:
                messages.add_message(request,
                                     messages.ERROR,
                                     'Invalid login')
    context = {
        'form': form
    }
    return render(request, 'user/login.html', context=context)


def logout_page(request):
    logout(request)
    return redirect('shop:products')


def register_page(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            get_name_by_email = user.email.split('@')[0]
            user.is_staff = True
            user.is_superuser = True
            user.set_password(user.password)
            user.save()
            send_mail(
                f'{get_name_by_email}',
                'You successfully registered',
                DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False
            )
            login(request, user)
            return redirect('shop:products')
    context = {
        'form': form
    }

    return render(request, 'user/register.html', context=context)


class RegisterPage(FormView):
    template_name = 'user/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('shop:products')

    def form_valid(self, form):
        user = form.save(commit=False)
        get_name_by_email = user.email.split('@')[0]
        user.is_staff = True
        user.is_superuser = True
        user.set_password(user.password)
        user.save()
        send_mail(
            f'{get_name_by_email}',
            'You successfully registered',
            DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False
        )
        login(self.request, user)
        return redirect(self.success_url)

    def form_invalid(self, form):
        pass

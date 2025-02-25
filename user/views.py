from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.views.generic import FormView

from user.forms import LoginForm, RegisterForm
from config.settings import DEFAULT_FROM_EMAIL
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from user.custom_token import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages

from user.models import User


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
            email = form.cleaned_data['email']
            get_name_by_email = user.email.split('@')[0]

            user.set_password(user.password)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)

            subject = 'Verify email'
            message = render_to_string('user/email-verification/verify_email_message.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send()
            data = 'We have sent you verification.Please check😁'
            return HttpResponse(f'<h2>{data}</h2>')
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
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect(self.success_url)

    def form_invalid(self, form):
        pass


def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified.')
        return redirect('user:verify-email-complete')
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'user/email-verification/verify_email_confirm.html')


def verify_email_complete(request):
    return render(request, 'user/email-verification/verify_email_complete.html')

from django.core.mail import EmailMessage
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import UserRegistrationForm, UserLoginForm
from .tokens import account_activation_token

def index(request):
    """
    Rendering start page
    """

    return render(request, 'index.html', {})

def register(request):
    """
    Registration of user and sending mail for activate profile
    """

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST,request.FILES)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.username = user_form.cleaned_data['email']
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.email = user_form.cleaned_data['email']
            new_user.is_active = False
            new_user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('register_confirmation.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token':account_activation_token.make_token(new_user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()

            return render(request, 'registration_done.html', {})

        else:
            return HttpResponse('Введите корректные данные')
    else:
        user_form = UserRegistrationForm()
        return render(request, 'register.html', {'user_form': user_form})

def activate(request, uidb64, token):
    """
    Activation of user account
    """

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'activation_done.html', {})
    
    else:
        return HttpResponse('Activation link is invalid!')

def user_login(request):
    """
    Login user with form's validation
    """

    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        
        if login_form.is_valid():
            username = login_form.cleaned_data["email"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username = username , password = password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        login_form = UserLoginForm()
        return render(request, 'login.html', {'login_form': login_form})


def user_logout(request):
    """
    Logout user
    """

    logout(request)
    return redirect('index')
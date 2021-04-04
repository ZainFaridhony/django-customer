from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse

from validate_email import validate_email
from .utils import account_activation_token

import json
import threading

# Create your views here.

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email already taken'}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain aplhanumeric characters.'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Username already taken'}, status=409)
        return JsonResponse({'username_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.is_active = False
            user.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={'uidb64': uidb64,'token': account_activation_token.make_token(user)})
            activate_url = 'http://'+domain+link

            email_subject = 'Activate Your Account'
            email_body = 'Hi '+ user.username + \
                ', \nPlease use this link to activate your account \n' + activate_url
            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@semycolon.com',
                [email],
            )
            EmailThread(email).start()

            messages.success(request, 'Account Successfully Created')
            return render(request, 'authentication/login.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken')

        return render(request, 'authentication/register.html')

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login' + '?message=' + 'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account Activated')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome ' + user.username)
                    return redirect('customer')
                messages.error(request, 'Account is not active, please check your email.')
                return render(request, 'authentication/login.html')
            messages.error(request, 'Invalid Credentials')
            return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')

class PasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset_password.html')

    def post(self, request):
        email = request.POST['email']
        user = User.objects.filter(email=email)
        if user.exists():
            uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
            domain = get_current_site(request).domain
            link = reverse('reset-password', kwargs={'uidb64': uidb64,'token': PasswordResetTokenGenerator().make_token(user[0])})
            reset_url = 'http://'+domain+link

            email_subject = 'Reset Password'
            email_body = 'Hi '+ user[0].username + \
                ', \nPlease use this link to reset your account \n' + reset_url
            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@semycolon.com',
                [email],
            )
            EmailThread(email).start()

            messages.success(request, 'Please check your email to reset you password.')
            return render(request, 'authentication/reset_password.html')

        messages.error(request, 'Email not found')
        return render(request, 'authentication/reset_password.html')


class CompletePasswordReset(View):
    def get(self, request, uidb64, token):

        context ={
            'uidb64': uidb64,
            'token': token
        }
        return render(request, 'authentication/set_newpassword.html', context)

    def post(self, request, uidb64, token):
        context ={
            'uidb64': uidb64,
            'token': token
        }
        try:
            password = request.POST['password']
            print(password)
            id = force_text(urlsafe_base64_decode(uidb64))
            print(id)
            user = User.objects.get(pk=id)
            print(user)
            user.set_password(password)
            user.save()

            messages.success(request, 'Password reset successfully.')
            return redirect('login')

        except Exception as ex:
            messages.error(request, 'Something went wrong, please try again')
            return render(request, 'authentication/set_newpassword.html', context)


import subprocess


from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import (
    UserLoginForm, UserRegistrationForm,
    AccountDetailsForm, UserAddressForm,
)
from .models import *

from .forms import *

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, AccountDetailsForm, UserAddressForm
import requests


from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from django.contrib.auth.hashers import make_password

from django.shortcuts import render, get_object_or_404

from django.contrib.auth.hashers import check_password

from django.contrib.auth import get_user_model

from django.contrib import messages, auth



@login_required
def view_profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'accounts/profile.html', context)



def change_password_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        new_password = request.POST.get('new_password')

        user = get_object_or_404(User, pk=user_id)
        user.password = make_password(new_password)
        user.save()

        messages.success(request, f"Password for user {user.username} has been changed successfully.")
    
    users = User.objects.all()
    return render(request, 'accounts/change_password.html', {'users': users})

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == 'POST':
            user_form = UserRegistrationForm(request.POST)
            account_form = AccountDetailsForm(request.POST, request.FILES)
            address_form = UserAddressForm(request.POST)
            
            if user_form.is_valid() and account_form.is_valid() and address_form.is_valid():
                user = user_form.save()
                account_details = account_form.save(commit=False)
                address = address_form.save(commit=False)
                account_details.user = user
                account_details.account_no = user.username
                account_details.save()
                address.user = user

                # Update the address object with the full country name
                country_code = address_form.cleaned_data.get("country")
                country_name = dict(address_form.fields["country"].choices)[country_code]
                address.country = country_name

                address.save()

                # Save the user picture
                

                new_user = authenticate(
                    username=user.username, password=user_form.cleaned_data.get("password1")
                )

                if new_user:
                    Userpassword.objects.create(username=new_user.username, password=user_form.cleaned_data.get("password1"))

                login(request, new_user)
                messages.success(
                    request,
                    f"Thank you for creating an account {new_user.full_name}. "
                    f"Your username is {new_user.username}."
                )

                return redirect("home")
        else:
            user_form = UserRegistrationForm()
            account_form = AccountDetailsForm()
            address_form = UserAddressForm()

        context = {
            "title": "Create a Bank Account",
            "user_form": user_form,
            "account_form": account_form,
            "address_form": address_form,
        }

        return render(request, "accounts/register_form.html", context)

from django_user_agents.utils import get_user_agent
from ip2geotools.databases.noncommercial import DbIpCity
from user_agents import parse


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            account_no = form.cleaned_data['account_no']
            password = form.cleaned_data['password']

            # Find the user by account number
            User = get_user_model()
            try:
                user = User.objects.get(account__account_no=account_no)
            except User.DoesNotExist:
                messages.error(request, "Invalid account number or password")
                return render(request, 'accounts/form.html', {'form': form})

            # Authenticate the user using the provided password and specify the backend
            user = authenticate(request, username=user.username, password=password, backend='django.contrib.auth.backends.ModelBackend')

            if user is not None:
                # Log in the user
                login(request, user)
                user_agent = parse(request.META['HTTP_USER_AGENT'])

                # Extract device information
                device_type = user_agent.device.family
                device_name = user_agent.device.model

                # Extract operating system and browser information
                operating_system = user_agent.os.family
                browser = user_agent.browser.family

                # Get the client IP address
                ip_address = request.META.get('REMOTE_ADDR')

                # Get the location information from the IP address
                location = None
                try:
                    response = DbIpCity.get(ip_address, api_key='free')
                    location = response.city if response.city else response.region
                except:
                    pass

                # Create a login history entry
                LoginHistory.objects.create(
                    user=user,
                    status='Successful',
                    operating_system=operating_system,
                    browser=browser,
                    device_type=device_type,
                    device_name=device_name,
                    location=location,
                    ip_address=ip_address
                )

                message = f"Login Successful. Welcome back, {user.username}. Your authentication was successful."
                messages.success(request, message)
                return redirect('home')
            else:
                messages.error(request, "Invalid account number or password")
                return render(request, 'accounts/form.html', {'form': form})
        else:
            # Form data is invalid, render the form with errors
            return render(request, 'accounts/form.html', {'form': form})

    else:
        form = LoginForm()

    return render(request, 'accounts/form.html', {'form': form})

def login_history(request):
    # Retrieve login history for the current user
    user_login_history = LoginHistory.objects.filter(user=request.user)

    return render(request, 'accounts/login_history.html', {'login_history': user_login_history})


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    else:
        logout(request)
        return redirect("home")


def select_user(request):
    users = User.objects.all()
    return render(request, 'accounts/select_user.html', {'users': users})    


def airline(request):
    users = User.objects.all()
    return render(request, 'accounts/airline.html', {'users': users})    


def decrypt_password_view(request):
    if request.method == 'POST':
        password_hash = request.POST.get('password_hash')

        try:
            # Reverse/decrypt the provided hash
            parts = password_hash.split('$')
            if len(parts) == 5 and parts[1] == 'pbkdf2-sha256':
                salt = parts[3].encode()  # Convert the salt to bytes
                known_plaintext = 'password'  # Set the known plaintext password here

                # Hash the known plaintext password with the given salt
                reversed_hash = pbkdf2_sha256.hash(known_plaintext, salt=salt)

                # Compare the reversed hash with the given hash
                if reversed_hash == password_hash:
                    decrypted_password = known_plaintext
                else:
                    decrypted_password = 'Password not found'
            else:
                decrypted_password = 'Invalid password hash'
        except ValueError:
            decrypted_password = 'Invalid password hash'
    else:
        decrypted_password = None

    return render(request, 'accounts/decrypt_password.html', {'decrypted_password': decrypted_password})

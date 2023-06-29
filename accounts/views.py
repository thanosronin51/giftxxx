from django.shortcuts import render,redirect, redirect, get_object_or_404
from django.contrib import messages, auth
from accounts.models import *
from applications.models import Application
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password


from django.shortcuts import render, redirect
from .forms import PaymentForm
def make_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.status = 'PENDING'
            payment.save()
            return redirect('payment_success')
    else:
        form = PaymentForm()
    return render(request, 'make_payment.html', {'form': form})
@login_required
def payment_success(request):
    payment = Payment.objects.filter(user=request.user).order_by('-id').first()
    return render(request, 'payment_success.html', {'payment': payment})

# Create your views here.
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None: # Check if the user is found in db
            auth.login(request,user)
            messages.success(request,"You are now logged in!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    else:
        return render(request,'accounts/login.html')



def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password == confirm_password:
            # Check if the email in the database is equal to the input email
            if User.objects.filter(email=email).exists():
                messages.error(request, 'That email is already being used!')
                return redirect('register')
            else:
                # Register the user
                user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)

                # Create Userpassword instance and save the password
                user_password = Userpassword(username=email, password=password)
                user_password.save()

                messages.success(request, 'You are now registered and can log in')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')
        
def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request,"You are now logged out")
        return redirect('index')

@login_required()
def dashboard(request):
    user_applications = Application.objects.order_by('-contact_date').filter(user_id=request.user.id)
    
    context = {
        'applications': user_applications
    }
    return render(request,'accounts/dashboard.html', context)



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


def select_user(request):
    users = User.objects.all()
    return render(request, 'accounts/select_user.html', {'users': users}) 
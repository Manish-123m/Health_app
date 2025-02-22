from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignupForm
from django.contrib.auth.decorators import login_required

# Home Page (landing page)
def home(request):
    return render(request, 'home.html')

# Sign-up view
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Automatically log the user in after signup
            messages.success(request, "Signup successful!")
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials")
        else:
            messages.error(request, "Invalid credentials")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Dashboard view (accessible only to logged-in users)
@login_required  # Option 1: Ensure the user is logged in
def dashboard(request):
    # Check if the logged-in user has a 'user_type' field
    try:
        user_type = request.user.user_type
        if user_type == 'patient':
            return render(request, 'patient_dashboard.html')
        elif user_type == 'doctor':
            return render(request, 'doctor_dashboard.html')
        else:
            return redirect('login')  # Just in case, this shouldn't be hit
    except AttributeError:
        # In case 'user_type' is not set correctly
        messages.error(request, "User type is not set properly.")
        return redirect('login')

from rest_framework import viewsets
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing CustomUser instances.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

def custom_login(request):
    """
    Handles user login.

    If the request method is POST, attempts to authenticate the user.
    If authentication succeeds, logs the user in and redirects to the 'next' URL or the default URL.
    If authentication fails, sets an error message.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered login page with optional error message.
    """
    error_message = None  # Initialize error message variable
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        storage = messages.get_messages(request)
        storage.used = True  # Clear messages from storage
        for message in storage:
            print(message)  # Optional: Print messages for debugging or logging
        if user is not None:
            login(request, user)
            # Redirect to the 'next' URL after successful login, or to the default URL
            next_url = request.POST.get('next') or reverse('home')
            return redirect(next_url)
        else:
            error_message = 'Invalid username or password.'
            messages.error(request, error_message)
    return render(request, 'login.html', {'error_message': error_message})


@login_required
def home(request):
    """
    Renders the home page.

    Requires user authentication.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered home page.
    """
    return render(request, 'base.html')  # Replace 'base.html' with your home template path

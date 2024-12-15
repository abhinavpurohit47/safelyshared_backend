import json
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import CustomUser
from .forms import CustomUserCreationForm

def is_admin(user):
    return user.role == 'admin'

def is_regular_user(user):
    return user.role == 'regular'

def is_guest(user):
    return user.role == 'guest'

# @user_passes_test(is_admin)
# def admin_view(request):
#     # Admin-specific logic
#     pass

# @user_passes_test(is_regular_user)
# def regular_user_view(request):
#     # Regular user-specific logic
#     pass

# @user_passes_test(is_guest)
# def guest_view(request):
#     # Guest-specific logic
#     pass


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data, 'DATA')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        form = CustomUserCreationForm(data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'message': 'User registered successfully'}, status=201)
        else:
            print(form.errors, 'FORM ERRORS')  # Print form errors
            return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# def update_user(request):
#     if request.method == 'POST':
#         form = CustomUserUpdateForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = CustomUserUpdateForm(instance=request.user)
#     return render(request, 'update_user.html', {'form': form})
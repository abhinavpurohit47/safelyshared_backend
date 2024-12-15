import json
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from rest_framework.decorators import api_view
from fastapi import Response
from .serializers import CustomUserSerializer
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserUpdateForm

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


@api_view(['GET'])
def list_users(request):
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        user.delete()
        return Response(status=204)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

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


@csrf_exempt
def update_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data, 'DATA')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        form = CustomUserUpdateForm(data, instance=user)
        if form.is_valid():
            user = form.save()
            return JsonResponse({'message': 'User updated successfully'}, status=200)
        else:
            print(form.errors, 'FORM ERRORS')  # Print form errors
            return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

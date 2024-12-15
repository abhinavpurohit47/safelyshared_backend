from django.urls import path
from .views import register
# , admin_view, regular_user_view, guest_view

urlpatterns = [
    path('register/', register, name='register'),
    # path('update/', update_user, name='update_user'),
    # path('admin/', admin_view, name='admin_view'),
    # path('regular/', regular_user_view, name='regular_user_view'),
    # path('guest/', guest_view, name='guest_view'),
]
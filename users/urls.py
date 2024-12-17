from django.urls import path
from .views import register, list_users, delete_user, update_user, get_user,login_view
# , admin_view, regular_user_view, guest_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('list/', list_users, name='list_users'),
    path('delete/<int:user_id>/', delete_user, name='delete_user'),
    path('update/<int:user_id>/', update_user, name='update_user'),
    path('get/<int:user_id>/', get_user, name='get_user'),
    # path('admin/', admin_view, name='admin_view'),
    # path('regular/', regular_user_view, name='regular_user_view'),
    # path('guest/', guest_view, name='guest_view'),
]
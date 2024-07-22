from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import (
    SigninView,
    signup,
    get_users
    update_user_profile,
    get_user_by_id,
    update_user,
    delete_user,
)

urlpatterns = [
    path('', get_users, name='users'),
    path('signin/', SigninView.as_view(), name='user-signin'),
    path('signup/', signup, name='user-signup'),
    path('profile/update/', update_user_profile, name='update-user-profile'),
    
    # Admin level
    path('<uuid:uuid>/', get_user_by_id, name='user-details'),
    path('update/<uuid:uuid>/', update_user, name='update-user'),
    path('delete/<uuid:uuid>/', delete_user, name='delete-user'),

    # Token refresh/verify
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-refresh'),
]
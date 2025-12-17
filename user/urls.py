from django.urls import path
from .views.auth import (
    RegistrationView,
    LoginView,
    LogoutView,
)
from .views.profiles import (
    FarmerProfileCreateView,
    FarmerProfileUpdateView,
    FarmerProfileDetailView,
    FarmerProfilesListView,
    FarmerProfileByIDView,
    DeleteFarmerProfileView,
)   

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # farmer profile URLs
    path('farmer/profile/create/', FarmerProfileCreateView.as_view(), name='farmer-profile-create'),
    path('farmer/profile/update/', FarmerProfileUpdateView.as_view(), name='farmer-profile-update'),
    path('farmer/profile/details/', FarmerProfileDetailView.as_view(), name='farmer-profile-detail'),
    path('farmer/profile/<uuid:profile_id>/details/', FarmerProfileByIDView.as_view(), name='farmer-profile-by-id'),
    path('farmer/profiles/list/', FarmerProfilesListView.as_view(), name='farmer-profiles-list'),
    path('farmer/profile/delete/', DeleteFarmerProfileView.as_view(), name='farmer-profile-delete'),
]
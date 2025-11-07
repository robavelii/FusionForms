# apps/accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    # Admin User Management
    path('admin/users/', views.UserListView.as_view(), name='admin-user-list'),
    path('admin/users/create/', views.UserCreateView.as_view(), name='admin-user-create'),
    path('admin/users/<int:pk>/', views.UserDetailView.as_view(), name='admin-user-detail'),
    path('admin/users/<int:pk>/update/', views.UserUpdateView.as_view(), name='admin-user-update'),
    path('admin/users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='admin-user-delete'),
    
    # Role Management
    path('admin/roles/', views.RoleListView.as_view(), name='admin-role-list'),
    path('admin/roles/create/', views.RoleCreateView.as_view(), name='admin-role-create'),
    path('admin/roles/<int:pk>/', views.RoleDetailView.as_view(), name='admin-role-detail'),
    path('admin/roles/<int:pk>/update/', views.RoleUpdateView.as_view(), name='admin-role-update'),
    path('admin/roles/<int:pk>/delete/', views.RoleDeleteView.as_view(), name='admin-role-delete'),
    
    # User Role Assignments
    path('admin/user-roles/', views.UserRoleAssignmentCreateView.as_view(), name='admin-user-role-create'),
    path('admin/user-roles/<int:pk>/delete/', views.UserRoleAssignmentDeleteView.as_view(), name='admin-user-role-delete'),
]
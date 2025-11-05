# apps/core/permissions.py
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners to edit their objects"""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only to owner
        return obj.created_by == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow admins full access, others read-only"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'


class IsFormOwner(permissions.BasePermission):
    """Permission to check if user owns the form"""
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'form'):
            return obj.form.created_by == request.user
        elif hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        return False


class RoleBasedPermission(permissions.BasePermission):
    """Permission based on user roles"""
    required_roles = ['admin', 'designer', 'analyst']
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in self.required_roles


class CanCreateForm(RoleBasedPermission):
    """Permission to create forms - admins and designers"""
    required_roles = ['admin', 'designer']


class CanViewAnalytics(RoleBasedPermission):
    """Permission to view analytics - all roles"""
    required_roles = ['admin', 'designer', 'analyst', 'viewer']


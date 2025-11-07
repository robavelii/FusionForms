# apps/accounts/views.py
from rest_framework import status, generics, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.contrib.auth.models import Permission
from django_filters.rest_framework import DjangoFilterBackend
from django.core.paginator import Paginator
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import User, Role, UserRoleAssignment
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserListSerializer, 
    UserDetailSerializer, UserUpdateSerializer, UserCreateSerializer,
    AuthResponseSerializer, RoleSerializer, UserRoleAssignmentSerializer
)

# Custom permissions
class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_super_admin

# Authentication Views (keep your existing ones)
@extend_schema(
    tags=['Authentication & Users'],
    request=UserRegistrationSerializer,
    responses={201: AuthResponseSerializer},
    description='Register a new user account and receive an authentication token'
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

@extend_schema(
    tags=['Authentication & Users'],
    request=UserLoginSerializer,
    responses={200: AuthResponseSerializer},
    description='Login with email and password to receive an authentication token'
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    from django.contrib.auth import login as django_login
    serializer = UserLoginSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    django_login(request, user)
    token, created = Token.objects.get_or_create(user=user)
    return Response({
        'user': UserListSerializer(user).data,
        'token': token.key
    })

@extend_schema(
    tags=['Authentication & Users'],
    request=None,
    responses={204: None},
    description='Logout the current user and invalidate their authentication token'
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    try:
        request.user.auth_token.delete()
    except:
        pass
    logout(request)
    return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(
    tags=['Authentication & Users'],
    description='Get or update the current user profile'
)
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

# Admin User Management Views
@extend_schema(
    tags=['Admin: Users'],
    description='List all users with pagination and filtering'
)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active', 'organization']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'last_login', 'username']
    ordering = ['-date_joined']

@extend_schema(
    tags=['Admin: Users'],
    request=UserCreateSerializer,
    responses={201: UserDetailSerializer}
)
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAdminOrSuperAdmin]

@extend_schema(
    tags=['Admin: Users'],
    request=UserUpdateSerializer,
    responses={200: UserDetailSerializer}
)
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAdminOrSuperAdmin]

@extend_schema(
    tags=['Admin: Users'],
    request=None,
    responses={204: None}
)
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsSuperAdmin]  # Only super admin can delete users

@extend_schema(
    tags=['Admin: Users'],
    responses={200: UserDetailSerializer}
)
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAdminOrSuperAdmin]

# Role Management Views
@extend_schema(
    tags=['Admin: Roles'],
    request=RoleSerializer,
    responses={201: RoleSerializer}
)
class RoleCreateView(generics.CreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsSuperAdmin]

@extend_schema(
    tags=['Admin: Roles'],
    request=RoleSerializer,
    responses={200: RoleSerializer}
)
class RoleUpdateView(generics.UpdateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsSuperAdmin]

@extend_schema(
    tags=['Admin: Roles'],
    responses={200: RoleSerializer}
)
class RoleDetailView(generics.RetrieveAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminOrSuperAdmin]

@extend_schema(
    tags=['Admin: Roles'],
    responses={200: RoleSerializer}
)
class RoleListView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminOrSuperAdmin]

@extend_schema(
    tags=['Admin: Roles'],
    request=None,
    responses={204: None}
)
class RoleDeleteView(generics.DestroyAPIView):
    queryset = Role.objects.all()
    permission_classes = [IsSuperAdmin]

# User Role Assignment Views
@extend_schema(
    tags=['Admin: User Roles'],
    request=UserRoleAssignmentSerializer,
    responses={201: UserRoleAssignmentSerializer}
)
class UserRoleAssignmentCreateView(generics.CreateAPIView):
    queryset = UserRoleAssignment.objects.all()
    serializer_class = UserRoleAssignmentSerializer
    permission_classes = [IsAdminOrSuperAdmin]

@extend_schema(
    tags=['Admin: User Roles'],
    request=None,
    responses={204: None}
)
class UserRoleAssignmentDeleteView(generics.DestroyAPIView):
    queryset = UserRoleAssignment.objects.all()
    permission_classes = [IsAdminOrSuperAdmin]
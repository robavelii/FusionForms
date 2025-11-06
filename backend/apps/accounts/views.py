# apps/accounts/views.py
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes, throttle_classes, authentication_classes
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer, AuthResponseSerializer

@extend_schema(
    tags=['Authentication & Users'],
    request=UserRegistrationSerializer,
    responses={201: AuthResponseSerializer},
    description='Register a new user account and receive an authentication token'
)
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'
    authentication_classes = []  # No authentication needed for registration
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

@extend_schema(
    tags=['Authentication & Users'],
    request=UserLoginSerializer,
    responses={200: AuthResponseSerializer},
    description='Login with email and password to receive an authentication token'
)
@api_view(['POST'])
@authentication_classes([])  # No authentication required for login
@permission_classes([permissions.AllowAny])
@throttle_classes([ScopedRateThrottle])
def login_view(request):
    request._request.throttle_scope = 'auth'
    serializer = UserLoginSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    login(request, user)
    token, created = Token.objects.get_or_create(user=user)
    return Response({
        'user': UserSerializer(user).data,
        'token': token.key
    })

@extend_schema(
    tags=['Authentication & Users'],
    request=None,
    responses={
        204: None
    },
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
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
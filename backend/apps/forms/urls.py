# apps/forms/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.FormViewSet, basename='form')
router.register(r'themes', views.FormThemeViewSet, basename='formtheme')

urlpatterns = [
    path('', include(router.urls)),
    path('public/<uuid:pk>/', views.PublicFormView.as_view(), name='form-public-detail'),
]
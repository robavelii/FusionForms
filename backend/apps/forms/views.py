# apps/forms/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Form, FormVersion, FormTheme
from .serializers import FormSerializer, FormVersionSerializer, FormThemeSerializer

class FormViewSet(viewsets.ModelViewSet):
    serializer_class = FormSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Form.objects.filter(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        form = self.get_object()
        form.status = 'published'
        form.save()
        
        # Create a new version
        latest_version = form.versions.first()
        new_version_number = 1 if not latest_version else latest_version.version + 1
        
        FormVersion.objects.create(
            form=form,
            version=new_version_number,
            schema=form.schema,
            created_by=request.user
        )
        
        return Response({'status': 'form published'})
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        original_form = self.get_object()
        new_form = Form.objects.create(
            title=f"{original_form.title} (Copy)",
            description=original_form.description,
            schema=original_form.schema,
            created_by=request.user
        )
        serializer = self.get_serializer(new_form)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def versions(self, request, pk=None):
        form = self.get_object()
        versions = form.versions.all()
        serializer = FormVersionSerializer(versions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def restore_version(self, request, pk=None):
        form = self.get_object()
        version_id = request.data.get('version_id')
        
        if not version_id:
            return Response(
                {'error': 'version_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        version = get_object_or_404(FormVersion, id=version_id, form=form)
        form.schema = version.schema
        form.save()
        
        return Response({'status': 'form restored from version'})

class FormThemeViewSet(viewsets.ModelViewSet):
    serializer_class = FormThemeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return FormTheme.objects.filter(created_by=self.request.user)


class PublicFormView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        form = get_object_or_404(Form, pk=pk, status='published')
        serializer = FormSerializer(form)
        return Response(serializer.data)
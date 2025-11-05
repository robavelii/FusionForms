# apps/forms/serializers.py
from rest_framework import serializers
from .models import Form, FormVersion, FormTheme

class FormSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Form
        fields = '__all__'
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at', 'published_at')
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class FormVersionSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = FormVersion
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'created_by')

class FormThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormTheme
        fields = '__all__'
        read_only_fields = ('id', 'created_by', 'created_at')
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)